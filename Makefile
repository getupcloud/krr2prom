KRR_VERSION  := 1.11.0
IMAGE_TAG    := 1.0.0
IMAGE_REPO   := getupcloud/krr2prom
IMAGE_NAME   := $(IMAGE_REPO):$(IMAGE_TAG)
IMAGE_LATEST := $(IMAGE_REPO):latest

build:
	docker build . -t $(IMAGE_NAME) --build-arg KRR_GIT_TAG=v$(KRR_VERSION)

tag:
	git tag v$(IMAGE_TAG)

release: build tag
	docker push $(IMAGE_NAME)
	docker push $(IMAGE_LATEST)
	git push origin v$(IMAGE_TAG):v$(IMAGE_TAG)
