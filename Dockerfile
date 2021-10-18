FROM python:3.9

# Install dependencies
RUN pip install streamlit plotly


WORKDIR /app
# add
ADD pyargent ./pyargent
# add streamlit component
ADD streamlit/app.py ./app.py
ADD streamlit/config.toml ./.streamlit/config.toml

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

# Expose port
EXPOSE 8001

CMD ["bash"]
