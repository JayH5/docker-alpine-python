#!/usr/bin/env bash
set -e

cd "$VERSION"

# Parse the image name from the onbuild Dockerfile and add the variant
IMAGE="$(awk '$1 == "FROM" { print $2; exit }' onbuild/Dockerfile)${VARIANT:+-$VARIANT}"

# Parse the version of Python from the Dockerfile
PYTHON_VERSION="$(awk '$2 == "PYTHON_VERSION" { print $3; exit }' ${VARIANT:+$VARIANT/}Dockerfile)"

function version_tags {
  local tag="$1"; shift
  local version="$1"; shift

  # Generate all variations of version (e.g. 5.3.1, 5.3, 5) and insert into tag
  local tags=()
  while [[ -n "$version" ]]; do
    tags+=("$version${tag:+-$tag}")
    version="$(echo "$version" | sed -E 's/[.-]?[[:alnum:]]+$//')"
  done

  echo "${tags[@]}"
}

function deploy {
  local image="$1"; shift

  local unversioned_tag="$(echo "${image##*:}" | sed -E "s/^$VERSION-?//")"
  local tags="$(version_tags "$unversioned_tag" "$PYTHON_VERSION")"
  docker-ci-deploy --tag $tags -- "$image"
}

# Login to Docker Hub
docker login -u "$REGISTRY_USER" -p "$REGISTRY_PASS"

# Deploy the image
deploy "$IMAGE"

# Deploy the onbuild image if we're building the standard image
if [[ -z "$VARIANT" ]]; then
  deploy "$IMAGE-onbuild"
fi
