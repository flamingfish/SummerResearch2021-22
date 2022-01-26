#!/usr/bin/env python
# coding: utf-8

# In[1]:


# requirements - python 3.9 and above
# pip install openhistorian


# In[137]:


import sys
import os

from openHistorian.historianConnection import historianConnection
from openHistorian.historianInstance import historianInstance
from openHistorian.historianKey import historianKey
from openHistorian.historianValue import historianValue
from openHistorian.metadataCache import metadataCache
from openHistorian.measurementRecord import SignalType
from snapDB.timestampSeekFilter import timestampSeekFilter
from snapDB.pointIDMatchFilter import pointIDMatchFilter
from typing import Optional, List
from datetime import datetime, timedelta
from time import time
import numpy as np

def readTest():
    # Create historian connection (the root API object)
    historian = historianConnection("10.35.0.216")
    instance: Optional[historianInstance] = None

    try:
        print("Connecting to openHistorian...")
        historian.Connect()

        if not historian.IsConnected or len(historian.InstanceNames) == 0:
            print("No openHistorian instances detected!")
        else:
            # Get first historian instance
            initialInstance = historian.InstanceNames[0]
        
            print(f"Opening \"{initialInstance}\" database instance...")
            instance = historian.OpenInstance(initialInstance)
                
            # Get a reference to the openHistorian metadata cache
            historian.RefreshMetadata()
            metadata = historian.Metadata

            
            pointIDList = []

            # Execute a test read for data archived ten seconds ago
            endTime = datetime.utcnow().replace(microsecond=0, second=0) - timedelta(minutes = 5)
            print(endTime)
            startTime = endTime - timedelta(minutes = 1)
            print(f"Starting read for {len(pointIDList):,} points from {startTime} to {endTime}...\r\n")
            print(pointIDList)
            
            # Each pmu measurement has a point id. Here i'm specifying the point id of a freq of a certain pmu
            # point ids can be found in th json list 
            pointIDList.append(13621)

            TestRead(instance, historian.Metadata, startTime, endTime, pointIDList)
    except Exception as ex:
        print(f"Failed to connect: {ex}")
    finally:
        if instance is not None:
            instance.Dispose()

        if historian.IsConnected:
            print("Disconnecting from openHistorian")
        
        historian.Disconnect()

def TestRead(instance: historianInstance, metadata: metadataCache, startTime: datetime, endTime: datetime, pointIDList: List[np.uint64]):
    timeFilter = timestampSeekFilter.CreateFromRange(startTime, endTime)
    pointFilter = pointIDMatchFilter.CreateFromList(pointIDList)

    opStart = time()
    reader = instance.Read(timeFilter, pointFilter)
    count = 0
                
    key = historianKey()
    value = historianValue()

    while reader.Read(key, value):
        count += 1
        print(f"    Point {key.ToString(metadata)} = {value.ToString()}")

    print(f"\r\nRead complete for {count:,} points in {(time() - opStart):.2f} seconds.\r\n")

if __name__ == "__main__":
    readTest()


# In[ ]:




