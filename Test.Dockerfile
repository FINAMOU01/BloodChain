FROM python:3.11-slim

# Test if web3 can be installed
RUN pip install web3==6.9.0
RUN python -c "import web3; print('web3 version:', web3.__version__)"

CMD ["python", "-c", "import web3; print('web3 found')"]
