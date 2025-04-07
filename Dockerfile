FROM quay.io/astronomer/astro-runtime:12.7.1

# Install dbt and dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt