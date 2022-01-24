run:
	@uvicorn api:app --host localho.st --reload --ssl-certfile=localho.st.pem --ssl-keyfile=localho.st-key.pem