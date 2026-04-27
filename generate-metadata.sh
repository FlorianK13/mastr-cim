#!/bin/bash

set -e

PROFILE_YML="schema/cim-mastr-data-profile.yml"
METADATA_JSON="metadata.json"

rm -f "$PROFILE_YML" "$METADATA_JSON"

gen-linkml-profile profile \
    -c WindGeneratingUnit \
    -c maxOperatingP \
    -c aggregate \
    -c normallyInService \
    -c PositionPoint \
    -c Length \
    schema/im_tc57cim.yml > "$PROFILE_YML"

linkml generate jsonld-context "$PROFILE_YML" > "$METADATA_JSON"