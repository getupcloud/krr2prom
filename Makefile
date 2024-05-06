IMAGE_TAG    := 2.3.0
IMAGE_REPO   := getupcloud/krr2prom
IMAGE_NAME   := $(IMAGE_REPO):$(IMAGE_TAG)
IMAGE_LATEST := $(IMAGE_REPO):latest
KRR_GIT_TAG  := v1.8.3

build:
	docker build . -t $(IMAGE_NAME) --build-arg KRR_GIT_TAG=$(KRR_GIT_TAG)

release: build
	docker push $(IMAGE_NAME)
	docker push $(IMAGE_LATEST)
