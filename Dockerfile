FROM zricethezav/gitleaks:latest AS gitleaks

FROM python:3.10-alpine3.16

WORKDIR /code

RUN apk add --no-cache bash curl

# copy Gitleaks binary from the first stage to the final image
COPY --from=gitleaks /usr/bin/gitleaks /usr/local/bin/gitleaks

COPY formatted_gitleaks.py /formatted_gitleaks.py
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

ENTRYPOINT ["python", "/formatted_gitleaks.py"]
