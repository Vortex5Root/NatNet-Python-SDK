import struct
from typing import Dict, Generator

class DataInjection:

    def __init__(self, packet : bytes) -> None:
        self.packet = packet

    def extract_Markers(self,nMarkers, stating_value) -> Generator:
        markers_list = []
        for nm_ in nMarkers:
            nm = nm_ + stating_value
            data = {
                "x" : struct.unpack("f", self.packet[nm+5]),
                "y" : struct.unpack("f", self.packet[nm+6]),
                "z" : struct.unpack("f", self.packet[nm+7]),
            }
            markers_list.append(data)
        return markers_list, nm

    def extract_RigidBodies(self, nRigidBodies, stating_value) -> Generator:
        rigid_bodies_list = []
        for nrb_ in nRigidBodies:
            nrb = nrb_ + stating_value
            data = {
                "iID" : struct.unpack("I", self.packet[nrb+1]),
                "szName" : self.packet[nrb+2],
                "nMarkers" : struct.unpack("I", self.packet[nrb+3]),
                "Markers" : self.extract_Markers(self.packet[nrb+4]),
            }
            rigid_bodies_list.append(data)
        return rigid_bodies_list, nrb

    def extract_sMarkerSetData(self, nMarkerSets, stating_value) -> Generator:
        smarkerset_list = []
        for nms_ in nMarkerSets:
            nms = nms_ + stating_value
            data = {
                "szName" : self.packet[nms],
                "nMarkers" : struct.unpack("I", self.packet[nms+1]),
                "Markers" : self.extract_Markers(self.packet[nms+2]),
            }
            smarkerset_list.append(data)
        return smarkerset_list, nms+2

    def extract_sSkeletonData(self, nSkeletons, stating_value) -> Generator:
        sskeleton_list = []
        for ns_ in nSkeletons:
            ns = ns_ + stating_value
            data = {
                "skeletonID" : self.packet[ns],
                "nRigidBodies" : struct.unpack("I", self.packet[ns+1]),
                "RigidBodies" : self.extract_RigidBodies(self.packet[ns+2]),
                "params" : self.packet[ns+3],
            }
            sskeleton_list.append(data)
        return sskeleton_list, ns

    def extract_Assets(self, nAssets, stating_value) -> Generator:
        extend_value = 0
        assets_list = []
        for na_ in nAssets:
            na = na_ + stating_value + extend_value

            data = {
                "assetID" : struct.unpack("I", self.packet[na]),
                "nRigidBodies" : struct.unpack("I", self.packet[na+1]),
                "RigidBodyData" : self.packet[na+2],
            }
            assets_list.append(data)
        '''
        assetID: int
    nRigidBodies: int
    RigidBodyData: List[sRigidBodyData]
    nMarkers: int
    MarkerData: List[sMarker]
        '''
    def inject(self, data : bytes) -> Dict:
        data_json = {}
        data_json["iFrame"] = struct.pack("I", self.packet[0])
        data_json["nMarkerSets"] = struct.pack("I", self.packet[1])
        data["sMarkerSetData"],index = self.extract_sMarkerSetData(self.packet[1],2)
        data_json["nOtherMarkers"] = struct.pack("I", self.packet[index+1])
        data_json["OtherMarkers"],index = self.extract_Markers(self.packet[index+1],index+2)
        data_json["nRigidBodies"] = struct.pack("I", self.packet[index+1])
        data["RigidBodies"],index = self.extract_RigidBodies(self.packet[index+1],index+2)
        data_json["nSkeletons"] = struct.pack("I", self.packet[index+1])
        data["Skeletons"],index = self.extract_sSkeletonData(self.packet[index+1],index+2)
        data["nAssets"] = struct.pack("I", self.packet[index+1])
        data["Assets"] = self.packet[index+2]
        return data_json