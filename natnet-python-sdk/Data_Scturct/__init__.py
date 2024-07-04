from typing import List
from pydantic import BaseModel

NAT_CONNECT = 0
NAT_SERVERINFO = 1
NAT_REQUEST = 2
NAT_RESPONSE = 3
NAT_REQUEST_MODELDEF = 4
NAT_MODELDEF = 5
NAT_REQUEST_FRAMEOFDATA = 6
NAT_FRAMEOFDATA = 7
NAT_MESSAGESTRING = 8
NAT_DISCONNECT = 9
NAT_KEEPALIVE = 10
NAT_DISCONNECTBYTIMEOUT = 11
NAT_ECHOREQUEST = 12
NAT_ECHORESPONSE = 13
NAT_DISCOVERY = 14
NAT_UNRECOGNIZED_REQUEST = 100

'''
// Client/server message ids
#define NAT_CONNECT                 0
#define NAT_SERVERINFO              1
#define NAT_REQUEST                 2
#define NAT_RESPONSE                3
#define NAT_REQUEST_MODELDEF        4
#define NAT_MODELDEF                5
#define NAT_REQUEST_FRAMEOFDATA     6
#define NAT_FRAMEOFDATA             7
#define NAT_MESSAGESTRING           8
#define NAT_DISCONNECT              9
#define NAT_KEEPALIVE               10
#define NAT_DISCONNECTBYTIMEOUT     11
#define NAT_ECHOREQUEST             12
#define NAT_ECHORESPONSE            13
#define NAT_DISCOVERY               14
#define NAT_UNRECOGNIZED_REQUEST    100


#define UNDEFINED                    999999.9999

'''

class MarkerData(BaseModel):
    x: float
    y: float
    z: float

class sMarkerSetData(BaseModel):
    szName: str
    nMarkers: int
    Markers: List[MarkerData]
'''
// MarkerSet Data (single frame of one MarkerSet)
typedef struct sMarkerSetData
{
    char szName[MAX_NAMELENGTH];            // MarkerSet name
    int32_t nMarkers;                       // # of markers in MarkerSet
    MarkerData* Markers;                    // Array of marker data ( [nMarkers][3] )
} sMarkerSetData;
'''
'''
// Marker Data
typedef struct MarkerData
{
    float x;                                // x position
    float y;                                // y position
    float z;                                // z position
    int16_t id;                             // Identifier
    float size;                             // Marker size
    int16_t params;                         // [reserved]
} MarkerData;
'''
class sRigidBodyData(BaseModel):
    iD: int
    szName: str
    x: float
    y: float
    z: float
    qx: float
    qy: float
    qz: float
    qw: float
    nMarkers: int
    MarkerData: List[MarkerData]
    MeanError: float
    params: int
'''
// Rigid Body Data (single frame of one rigid body)
typedef struct sRigidBodyData
{
    int32_t ID;                             // RigidBody identifier: 
                                            // For rigid body assets, this is the Streaming ID value. 
                                            // For skeleton assets, this combines both skeleton ID (High-bit) and Bone ID (Low-bit).

    float x, y, z;                          // Position
    float qx, qy, qz, qw;                   // Orientation
    float MeanError;                        // Mean measure-to-solve deviation (mean marker error) (meters)
    int16_t params;                         // Host defined tracking flags
'''
class sSkeletonData(BaseModel):
    skeletonID: int
    nRigidBodies: int
    RigidBodies: List[sRigidBodyData]
    params: int
'''
// Skeleton Data
typedef struct sSkeletonData
{
    int32_t skeletonID;                                     // Skeleton unique identifier
    int32_t nRigidBodies;                                   // # of rigid bodies
    sRigidBodyData* RigidBodyData;                          // Array of RigidBody data
} sSkeletonData;
'''
class sMarker(BaseModel):
    ID: int
    x: float
    y: float
    z: float
    size: float
    params: int
    residual: float
'''
// Marker
typedef struct sMarker
{
    int32_t ID;                             // Unique identifier:
                                            // For active markers, this is the Active ID. For passive markers, this is the PointCloud assigned ID.
                                            // For legacy assets that are created prior to 2.0, this is both AssetID (High-bit) and Member ID (Lo-bit)

    float x;                                // x position
    float y;                                // y position
    float z;                                // z position
    float size;                             // marker size
    int16_t params;                         // host defined parameters.  Bit values:
                                                // 0 : Occluded
                                                // 1 : PointCloudSolved
                                                // 2 : ModelFilled
                                                // 3 : HasModel
                                                // 4 : Unlabeled
                                                // 5 : Active
                                                // 6 : Established
                                                // 7 : Measurement
    float residual;                         // marker error residual, in m/ray
} sMarker;
'''
class sAssetData(BaseModel):
    assetID: int
    nRigidBodies: int
    RigidBodyData: List[sRigidBodyData]
    nMarkers: int
    MarkerData: List[sMarker]
'''
// Asset Data
typedef struct sAssetData
{
    int32_t assetID;                                        // User defined ID (correlates to sAssetDescription )
    
    int32_t nRigidBodies;                                   // # of rigid bodies
    sRigidBodyData* RigidBodyData;                          // Array of RigidBody data

    int32_t nMarkers;                                       // # of markers
    sMarker* MarkerData;                                    // Array of marker data

} sAssetData;
'''
class sAnalogChannelData(BaseModel):
    nFrames: int
    Values: List[float]
'''
typedef struct sAnalogChannelData
{
    int32_t nFrames;                                // # of analog frames of data in this channel data packet (typically # of subframes per mocap frame)
    float Values[MAX_ANALOG_SUBFRAMES];             // values
} sAnalogChannelData;
'''
class sForcePlateData(BaseModel):
    ID: int
    nChannels: int
    ChannelData: List[sAnalogChannelData]
    params: int
'''
typedef struct sForcePlateData
{
    int32_t ID;                                         // ForcePlate ID (from data description)
    int32_t nChannels;                                  // # of channels (signals) for this force plate
    sAnalogChannelData ChannelData[MAX_ANALOG_CHANNELS];// Channel (signal) data (e.g. Fx[], Fy[], Fz[])
    int16_t params;                                     // Host defined flags
} sForcePlateData;
'''
class sDeviceData(BaseModel):
    ID : int
    nChannels: int
    ChannelData: List[sAnalogChannelData]
    params: int
'''
typedef struct sDeviceData
{
    int32_t ID;                                         // Device ID (from data description)
    int32_t nChannels;                                  // # of active channels (signals) for this device
    sAnalogChannelData ChannelData[MAX_ANALOG_CHANNELS];// Channel (signal) data (e.g. ai0, ai1, ai2)
    int16_t params;                                     // [b0:trigger bit] [b1:reserved] [b2:is synthetic data?] [b3,b4: mocap frame offset]
} sDeviceData;
'''
class sFrameOfMocapData(BaseModel):
    iFrame: int
    nMarkerSets: int
    MocapData: List[sMarkerSetData]
    nOtherMarkers: int
    OtherMarkers: List[MarkerData]
    nRigidBodies: int
    RigidBodies: List[sRigidBodyData]
    nSkeletons: int
    Skeletons: List[sSkeletonData]
    nAssets: int
    Assets: List[sAssetData]
    nLabeledMarkers: int
    LabeledMarkers: List[sMarker]
    nForcePlates: int
    ForcePlates: List[sForcePlateData]
    nDevices: int
    Devices: List[sDeviceData]
    Timecode: int
    TimecodeSubframe: int
    fTimestamp: float
    CameraMidExposureTimestamp: int
    CameraDataReceivedTimestamp: int
    TransmitTimestamp: int
    PrecisionTimestampSecs: int
    PrecisionTimestampFractionalSecs: int
    params: int

''' (NatNetTypes.h) [line 479]
// Single frame of data (for all tracked objects)
typedef struct sFrameOfMocapData
{
    int32_t iFrame;                                 // host defined frame number

    int32_t nMarkerSets;                            // # of marker sets in this frame of data
    sMarkerSetData MocapData[MAX_MARKERSETS];       // MarkerSet data

    int32_t nOtherMarkers;                          // # of undefined markers
    MarkerData* OtherMarkers;                       // undefined marker data

    int32_t nRigidBodies;                           // # of rigid bodies
    sRigidBodyData RigidBodies[MAX_RIGIDBODIES];    // Rigid body data

    int32_t nSkeletons;                             // # of Skeletons
    sSkeletonData Skeletons[MAX_SKELETONS];         // Skeleton data

    int32_t nAssets;                                // # of Assets
    sAssetData Assets[MAX_ASSETS];                  // Asset data

    int32_t nLabeledMarkers;                        // # of Labeled Markers
    sMarker LabeledMarkers[MAX_LABELED_MARKERS];    // Labeled Marker data (labeled markers not associated with a "MarkerSet")

    int32_t nForcePlates;                           // # of force plates
    sForcePlateData ForcePlates[MAX_FORCEPLATES];   // Force plate data

    int32_t nDevices;                               // # of devices
    sDeviceData Devices[MAX_DEVICES];               // Device data

    uint32_t Timecode;                              // SMPTE timecode (if available)
    uint32_t TimecodeSubframe;                      // timecode sub-frame data
    double fTimestamp;                              // timestamp since software start ( software timestamp )
    uint64_t CameraMidExposureTimestamp;            // Given in host's high resolution ticks (from e.g. QueryPerformanceCounter).
    uint64_t CameraDataReceivedTimestamp;           // Given in host's high resolution ticks (from e.g. QueryPerformanceCounter).
    uint64_t TransmitTimestamp;                     // Given in host's high resolution ticks (from e.g. QueryPerformanceCounter).
    uint32_t PrecisionTimestampSecs;                // External precision timestamp (if present, e.g. PTP).
    uint32_t PrecisionTimestampFractionalSecs;      // External precision timestamp (if present, e.g. PTP).
    int16_t params;                                 // [b0: recording] 
                                                    // [b1: model list changed]
                                                    // [b2: Live/Edit mode (0=Live, 1=Edit)]
                                                    // [b3: bitstream version changed]
} sFrameOfMocapData;
'''