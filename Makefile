IMAGE_TAG  := 0.0.7
IMAGE_REPO := getupcloud/krr2prom
IMAGE_NAME := $(IMAGE_REPO):$(IMAGE_TAG)
IMAGE_LATEST := $(IMAGE_REPO):latest

build:
	docker build . -t $(IMAGE_NAME)

release: test build
	docker push $(IMAGE_NAME)
	docker push $(IMAGE_LATEST)

test:
	python krr2prom.py < test-data.json
