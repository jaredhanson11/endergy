FROM jaredhanson11/serverbase

# Allows requirements to be downloaded from custom pypi
ARG PIP_EXTRA_INDEX_URL

# Install required packages
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache -r requirements.txt \
    && rm requirements.txt

# Copy server code to the /app/ dir
COPY ./server ./server
