#!/usr/bin/env python3
from opendbc.can.parser import CANParser
from cereal import car
from selfdrive.car.toyota.values import NO_DSU_CAR, DBC, TSS2_CAR, RADAR_ACC_CAR_TSS1
from selfdrive.car.interfaces import RadarInterfaceBase
from common.params import Params

def _create_radar_can_parser(car_fingerprint):
    if DBC[car_fingerprint]['radar'] is None:
        return None

    signals = []
    checks = []

    if car_fingerprint in TSS2_CAR:
        RADAR_A_MSGS = list(range(0x180, 0x190))
        RADAR_B_MSGS = list(range(0x190, 0x1a0))

        msg_a_n = len(RADAR_A_MSGS)
        msg_b_n = len(RADAR_B_MSGS)

        signals += list(zip(['LONG_DIST'] * msg_a_n + ['NEW_TRACK'] * msg_a_n + ['LAT_DIST'] * msg_a_n +
                            ['REL_SPEED'] * msg_a_n + ['VALID'] * msg_a_n + ['SCORE'] * msg_b_n,
                            RADAR_A_MSGS * 5 + RADAR_B_MSGS))

        checks += list(zip(RADAR_A_MSGS + RADAR_B_MSGS, [20] * (msg_a_n + msg_b_n)))
    else:
        if Params().get_bool("ToyotaRadarACCTSS1_ObjectMode"):
            RADAR_A_MSGS = list(range(0x301, 0x318, 2))
        else:
            RADAR_A_MSGS = list(range(0x680, 0x686))

        msg_n = len(RADAR_A_MSGS)

        signals += list(zip(
            ['ID'] * msg_n + ['LONG_DIST'] * msg_n + ['LAT_DIST'] * msg_n + ['SPEED'] * msg_n +
            ['LAT_SPEED'] * msg_n,
            RADAR_A_MSGS * 5))

        checks += list(zip(RADAR_A_MSGS, [15] * msg_n))

    return CANParser(DBC[car_fingerprint]['radar'], signals, checks, 1)


class RadarInterface(RadarInterfaceBase):
  def __init__(self, CP):
    super().__init__(CP)
    self.track_id = 0
    self.radar_ts = CP.radarTimeStep
    self.radar_acc_tss1 = CP.carFingerprint in RADAR_ACC_CAR_TSS1

    if self.radar_acc_tss1:
      if Params().get_bool("ToyotaRadarACCTSS1_ObjectMode"):
        self.RADAR_A_MSGS = self.RADAR_B_MSGS = list(range(0x301, 0x318, 2))
      else:
        self.RADAR_A_MSGS = self.RADAR_B_MSGS = list(range(0x680, 0x686))
      self.valid_cnt = {key: 0 for key in range(0x3f)}
    else:
      if CP.carFingerprint in TSS2_CAR:
        self.RADAR_A_MSGS = list(range(0x180, 0x190))
        self.RADAR_B_MSGS = list(range(0x190, 0x1a0))
      else:
        self.RADAR_A_MSGS = list(range(0x210, 0x220))
        self.RADAR_B_MSGS = list(range(0x220, 0x230))
      self.valid_cnt = {key: 0 for key in self.RADAR_A_MSGS}

    self.rcp = _create_radar_can_parser(CP.carFingerprint)
    self.trigger_msg = self.RADAR_B_MSGS[-1]
    self.updated_messages = set()

    # No radar dbc for cars without DSU which are not TSS 2.0
    # TODO: re-add no_dsu for cars without canfilter

  def update(self, can_strings):
    if self.rcp is None:
      return super().update(None)

    vls = self.rcp.update_strings(can_strings)
    self.updated_messages.update(vls)

    if self.trigger_msg not in self.updated_messages:
      return None

    rr = self._update(self.updated_messages, is_tss1=self.radar_acc_tss1)
    self.updated_messages.clear()

    return rr

  def _update(self, updated_messages, is_tss1=False):
    ret = car.RadarData.new_message()
    errors = []
    if not self.rcp.can_valid:
        errors.append("canError")
    ret.errors = errors

    for ii in sorted(updated_messages):
        if ii not in self.RADAR_A_MSGS:
          continue
        cpt = self.rcp.vl[ii]
        if is_tss1:
            if cpt['ID'] == 0x3f or cpt['LONG_DIST'] <= 0:
                continue
            track_id = int(cpt['ID'])
            self._update_radar_point(track_id, cpt)
        else:
            if cpt['LONG_DIST'] >= 255 or cpt['VALID'] == 0:
                continue
            self._update_radar_point(ii, cpt)

    ret.points = list(self.pts.values())
    return ret

  def _update_radar_point(self, track_id, cpt):
      if track_id not in self.pts or (not self.pts[track_id].measured):
          self.pts[track_id] = car.RadarData.RadarPoint.new_message()
          self.pts[track_id].trackId = self.track_id
          self.track_id += 1

      self.pts[track_id].dRel = cpt['LONG_DIST']  # from front of car
      self.pts[track_id].yRel = cpt['LAT_DIST']  # in car frame's y axis, left is positive
      self.pts[track_id].vRel = cpt['SPEED']  # it's absolute speed
      self.pts[track_id].aRel = float('nan')
      self.pts[track_id].yvRel = cpt['LAT_SPEED']
      self.pts[track_id].measured = True
