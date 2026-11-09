from langgraph.graph import StateGraph,START,END,MessagesState

from langgraph.prebuilt import ToolNode,tools_condition


from app.llm import llm

from app.tools import (metro_fare_tool,metro_route_tool,metro_station_tool)



tools = [
    metro_station_tool,
    metro_route_tool,
    metro_fare_tool
]

llm_with_tools = llm.bind_tools(tools)


def assistant(state:MessagesState):
    system_message = {
        "role":"system",
        "content":"""
        You are an AI Metro Assistant.
        
        Your responsibility is to answer only questions related to the fictional metro network.
        
        You can help users with:
        
        1. Metro routes and directions.
        2. Metro ticket fares.
        3. Metro station information.
        4. Conntected stations.
        5. Interchange stations.
        6. Mtero network infomation.
        
        STRICT RULES:
        1. Only answer metro-related questions.
        2. If this user asks anythings unrelated to the metro systems , politely respond:
        
        "Sorry, I can only assist with metro related questions , Please ask me something about the metro network."
        
        3. Never invent metro stations, routes or fares.
        4. If a station does not exists in the network,clearly explain that it is an unknown station.
        
        5.Be friendly , concise and helpful.
        
        IMPORTANT:
        If a question is not related to the metro network,
        do not use any tools and do not answers the question.
        
        """
        
        
        
    }
    
    messages = [system_message] + state["messages"]
    
    res = llm_with_tools.invoke(messages)
    return {
        "messages":[res]
    }
    
    
    
    
builder = StateGraph(MessagesState)


builder.add_node("assistant",assistant)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START,"assistant")

builder.add_conditional_edges("assistant",tools_condition)

builder.add_edge("tools","assistant")


metro_graph = builder.compile()