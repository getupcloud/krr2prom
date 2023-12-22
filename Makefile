IMAGE_TAG  := 2.0.0-beta12
IMAGE_REPO := getupcloud/krr2prom
IMAGE_NAME := $(IMAGE_REPO):$(IMAGE_TAG)
IMAGE_LATEST := $(IMAGE_REPO):latest

build:
	docker build . -t $(IMAGE_NAME)

release: build
	docker push $(IMAGE_NAME)
	docker push $(IMAGE_LATEST)
