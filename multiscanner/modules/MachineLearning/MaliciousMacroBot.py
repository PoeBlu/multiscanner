# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

__authors__ = "Austin West"
__license__ = "MPL 2.0"

TYPE = "MachineLearning"
NAME = "MaliciousMacroBot"
REQUIRES = ['libmagic']
DEFAULTCONF = {
    'ENABLED': False
}

try:
    from mmbot import MaliciousMacroBot
    has_mmbot = True
except ImportError as e:
    print("mmbot module not installed...")
    has_mmbot = False


def check(conf=DEFAULTCONF):
    return bool(has_mmbot) if conf['ENABLED'] else False


def scan(filelist, conf=DEFAULTCONF):
    results = []

    mmb = MaliciousMacroBot()
    mmb.mmb_init_model()

    for fname in filelist:
        # Ensure libmagic returns results
        if REQUIRES[0] is not None and 'Microsoft' in _get_libmagicresults(
            REQUIRES[0][0], fname
        ):
            result = mmb.mmb_predict(fname, datatype='filepath')
            prediction = result.iloc[0].get('prediction', None)
            confidence = result.iloc[0].get('result_dictionary', {}).get('confidence')
            result_dict = {
                'Prediction': prediction,
                'Confidence': confidence
            }
            results.append((fname, result_dict))

    metadata = {"Name": NAME, "Type": TYPE}
    return (results, metadata)


def _get_libmagicresults(results, fname):
    libmagicdict = dict(results)
    return libmagicdict.get(fname)
