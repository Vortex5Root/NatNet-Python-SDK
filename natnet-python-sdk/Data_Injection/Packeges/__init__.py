

import struct

class Struct_Tool:
    def unpack_vector3(self, data):
        return struct.unpack('<fff', data)
    
    def unpack_vector2(self, data):
        return struct.unpack('<ff', data)
    
    def unpack_quaternion(self, data):
        return struct.unpack('<ffff', data)
    
    def unpack_float_value(self, data):
        return struct.unpack('<f', data)
    
    def unpack_double_value(self, data):
        return struct.unpack('<d', data)
    
    def unpack_int_value(self, data):
        return struct.unpack('<I', data)
    
    def unpack_fp_cal_matrix_row(self, data):
        return struct.unpack('<ffffffffffff', data)
    
    def unpack_fp_corners(self, data):
        return struct.unpack('<ffffffffffff', data)


class Struct_Socket_Data:
    def __init__(self) -> None:
        self.struct_tool = Struct_Tool()

    def unpack_Marker(self, data : bytes, pointer : int, nMarkers : int):
        data = {}
        for nm in range(nMarkers):
            data["x"] = self.struct_tool.unpack_float_value(data[pointer+nm])
            data["y"] = self.struct_tool.unpack_float_value(data[pointer+nm+1])
            data["z"] = self.struct_tool.unpack_float_value(data[pointer+nm+2])
        return data, pointer+(3*nMarkers)

    def unpack_MarkerSet(self, data : bytes,pointer : int, nMarkersSets : int):
        data = {}
        for nms in range(nMarkersSets):
            data["szName"] = data[pointer+nms]
            data["nMarkers"] = self.struct_tool.unpack_int_value(data[pointer+nms+1])
            data["Markers"],pointer = self.unpack_Marker(data, pointer+nms+3, data["nMarkers"])
        return data, pointer
    
    def unpack_RigidBody(self, data : bytes, pointer : int, nRigidBodies : int):
        data = {}
        for nrb in range(nRigidBodies):
            data["iD"] = self.struct_tool.unpack_int_value(data[pointer])
            data["x"] = self.struct_tool.unpack_float_value(data[pointer+1])
            data["y"] = self.struct_tool.unpack_float_value(data[pointer+2])
            data["z"] = self.struct_tool.unpack_float_value(data[pointer+3])
            data["qx"] = self.struct_tool.unpack_float_value(data[pointer+4])
            data["qy"] = self.struct_tool.unpack_float_value(data[pointer+5])
            data["qz"] = self.struct_tool.unpack_float_value(data[pointer+6])
            data["qw"] = self.struct_tool.unpack_float_value(data[pointer+7])
            data["nMarkers"] = self.struct_tool.unpack_int_value(data[pointer+8])
            data["Markers"], pointer = self.unpack_Marker(data, pointer+9, data["nMarkers"])
        return data, pointer

    def unpack_sFrameOfMocapData(self, data : bytes):
        data = {}
        index = 0
        data["iframe"] = self.struct_tool.unpack_int_value(data[0])
        data["nMarkerSets"] = self.struct_tool.unpack_int_value(data[1])
        data["MarkerSets"], index = self.unpack_MarkerSet(data, 2, data["nMarkerSets"])
        data["nOtherMarkers"] = self.struct_tool.unpack_int_value(data[index])
        data["OtherMarkers"], index = self.unpack_Marker(data, index+1, data["nOtherMarkers"])
        data["nRigidBodies"] = self.struct_tool.unpack_int_value(data[index])
        data["RigidBodies"], index = self.unpack_RigidBody(data, index+1, data["nRigidBodies"])
        data["nSkeletons"] = self.struct_tool.unpack_int_value(data[index])
        data["Skeletons"], index = self.unpack_RigidBody(data, index+1, data["nSkeletons"])
        
'''

'''