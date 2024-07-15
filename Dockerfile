FROM cypress/browser:latest
RUN apt-get install python 3 -y
RUN echo $(python -m site --user-base)
COPY requirments.txt .
ENV PATH /home/root/ .Local/bin:${PATH}
RUN apt-get update && apt-get install -y python3-pip && pip install -r requirements.txt
COPY . .
CMD uvicorn main:app --host 0.0.0.0 --port $PORT