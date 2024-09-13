
include .env

all:
	python gen.py

	mv *.parquet data/

	$(MAKE) drop TABLE=Clickstream
	$(MAKE) drop TABLE=Product
	$(MAKE) drop TABLE=Purchase
	$(MAKE) drop TABLE=User

	$(MAKE) create TABLE=Clickstream FILE=clickstream
	$(MAKE) create TABLE=Product FILE=product
	$(MAKE) create TABLE=Purchase FILE=purchase
	$(MAKE) create TABLE=User FILE=user

	$(MAKE) upload TABLE=Clickstream FILE=clickstream_events
	$(MAKE) upload TABLE=Product FILE=products
	$(MAKE) upload TABLE=Purchase FILE=purchases
	$(MAKE) upload TABLE=User FILE=users

upload:
	@docker run \
		-v ${PWD}:/tmp/work/ \
		apachepinot/pinot:1.1.0 \
			LaunchDataIngestionJob \
			-jobSpecFile /tmp/work/jobs/job.yaml \
			-authToken " Bearer ${PINOT_TOKEN}" \
			-values PINOT_WORKSPACE=${PINOT_WORKSPACE} \
			-values PINOT_CONTROLLER=${PINOT_CONTROLLER} \
			-values TABLE=${TABLE} \
			-values FILE=${FILE} \
			-values DATA=/tmp/work/data/


create:
	@curl -X POST ${PINOT_CONTROLLER}/schemas \
		-H "Accept: application/json" \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer ${PINOT_TOKEN}" \
		-H "Database: ${PINOT_WORKSPACE}" \
		-d @conf/${FILE}-schema.json \
		| jq

	@curl -X  POST ${PINOT_CONTROLLER}/tables \
		-H "Accept: application/json" \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer ${PINOT_TOKEN}" \
		-H "Database: ${PINOT_WORKSPACE}" \
		-d @conf/${FILE}-table.json \
		| jq

drop:
	@curl -X DELETE ${PINOT_CONTROLLER}/schemas/${TABLE} \
		-H "Accept: application/json" \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer ${PINOT_TOKEN}" \
		-H "Database: ${PINOT_WORKSPACE}" \
		| jq

	@curl -X  DELETE ${PINOT_CONTROLLER}/tables/${TABLE} \
		-H "Accept: application/json" \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer ${PINOT_TOKEN}" \
		-H "Database: ${PINOT_WORKSPACE}" \
		| jq
