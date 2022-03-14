FROM python:3

ADD ec2_instance_data.py /

RUN pip install flask python

CMD [ "python", "./ec2_instance_data.py" ]

