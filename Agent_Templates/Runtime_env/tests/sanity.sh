curl -X POST \
  	-H "Content-Type: application/json" \
  	-d '{
    	"input": {
      		"messages": [
    			{
					"type": "human",
					"content": "What is the capital of France?"
				}
			],
			"user_id": "user123",
			"session_id": "session456"
		}
	}' \
	http://localhost:8000/chats