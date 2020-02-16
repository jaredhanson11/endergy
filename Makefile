images-dir=./modules
images=$(shell ls ${images-dir})
libs-dir=./lib
# Exclude setup.py as a lib
libs=$(shell ls ${libs-dir} | grep -v "setup.py")

build-images:
	$(foreach image, ${images}, $(MAKE) -C ${images-dir}/${image} build;)
push-images:
	$(foreach image, ${images}, $(MAKE) -C ${images-dir}/${image} push;)
build-libs:
	$(foreach lib, ${libs}, /scripts/python/python-build.sh ${libs-dir}/${lib};)
push-libs:
	$(foreach lib, ${libs}, /scripts/python/python-push.sh ${libs-dir}/${lib};)
