# from fastapi import FastAPI
# from pydantic import BaseModel
# from backend.chatbot import chatbot_response  # Import the chatbot logic
# from fastapi import FastAPI
# from backend.chatbot import chatbot_response


# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Backend running successfully!"}

# class ChatbotInput(BaseModel):
#     user_input: str

# # Define the request body schema for the chatbot endpoint
# class ChatbotRequest(BaseModel):
#     user_input: str

# # API endpoint for chatbot
# @app.post("/chatbot")
# def chatbot_endpoint(request: ChatbotRequest):
#     user_input = request.user_input
#     response = chatbot_response(user_input)
#     return {"response": response}

# # Define the request body schema for the route calculation endpoint
# class RouteRequest(BaseModel):
#     start: str
#     end: str

# # API endpoint for route calculation
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Dei-GO API! The server is running."}

# @app.post("/api/route")
# def get_route(request: RouteRequest):
#     start = request.start
#     end = request.end

#     if not start or not end:
#         raise HTTPException(status_code=400, detail="Start and end locations are required.")

#     result = find_shortest_path(G, start, end)
#     return result
# @app.post("/chatbot")
# def chatbot_endpoint(input: ChatbotInput):
#     user_input = input.user_input
#     print(f"Debug: Received input: {user_input}")  # Debug log
#     response = chatbot_response(user_input)
#     return {"response": response}

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Dei-GO API! The server is running."}



# print("✅ FastAPI app initialized successfully!")

