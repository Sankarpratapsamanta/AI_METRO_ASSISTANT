from collections import deque
from langchain.tools import tool

from app.metro_data import METRO_NETWORK,INTERCHANGE_STATIONS


def find_shortest_route(source:str,destination:str):
    source = source.strip()
    destination = destination.strip()
    
    if source not in METRO_NETWORK:
        return {
            "error":f"Unknown station :{source}"
        }
    if destination not in METRO_NETWORK:
        return {
            "error":f"Unknown station : {destination}"
        }
    
    if source == destination:
        return {
            "route":[source],
            "total_stations":1,
            "total_segments":0
        }
        
    queue = deque([[source]])
    visited = {source}
    
    while queue:
        route = queue.popleft()
        current_station = route[-1]
        
        for neighbor in METRO_NETWORK[current_station]:
            if neighbor in visited:
                continue
            new_route = route + [neighbor]
            
            if neighbor == destination:
                return {
                    "route":new_route,
                    "total_stations":len(new_route),
                    "total_segments":len(new_route) - 1
                }
            visited.add(neighbor)
            queue.append(new_route)
            
    return {
        "error":"No route found"
    }
    

def calculate_fare(source:str,destination:str):
    result = find_shortest_route(source,destination)
    
    if "error" in result:
        return result
    
    segments = result["total_segments"]
    
    fare = 10 + (segments * 5)
    
    return {
        "source":source,
        "destination":destination,
        "segments":segments,
        "fare":fare,
        "currency":"INR"
    }
    
def get_station_info(station:str):
    station = station.strip()
    
    if station not in METRO_NETWORK:
        return {
            "error":f"Unknown station: {station}"
        }
    return{
        "station":station,
        "connected_stations":METRO_NETWORK[station],
        "is_interchange":(
            station in INTERCHANGE_STATIONS
        )
    }
    
    

@tool
def metro_fare_tool(source:str,destination:str):
    """
    Calculate metro ticket fare between two stations.
    
    Use this tool when the user askes about ticket price or fare.
    """
    
    return calculate_fare(source,destination)


@tool
def metro_route_tool(source:str,destination:str):
    """
    Find the shortest metro route between two stations.
    
    Use this tool when the user asks for metro directions or a route.
    """
    
    return find_shortest_route(source,destination)

@tool
def metro_station_tool(station:str):
    """
    Get information about a metro station including connected stations and whether it is an interchange station.
    
    Use this tool for station-related questions.
    """
    
    return get_station_info(station)