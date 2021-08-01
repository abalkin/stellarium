from collections import Counter
NAMES_PATH = '../../stars/default/name.fab'
CROSS_ID = '../../stars/default/cross-id.dat'
CAT_FIELDS = {
    'PNo' : (0, 4, int),            # [1/1028]? Unique star number
    'PCon': (5, 8, str),            # ?Ptolemy constellation
    'PInf': (8, 9, str),            # [~]? ~ if 'informis'
    'PNum': (9, 11, int),           # ?Ptolemy number in constellation
   'w_Pto': (11, 12, str),          # [*]? Warning about this entry
    'LO.z': (12, 14, int),          # [0/11]? Longitude A.D. 137 Zodiac sign
    'LO.d': (15, 17, int),          # ?Longitude (degrees) within zodiac sign
    'w_LO': (17, 18, str),          # [*]? Warning about longitude 
    'LO.m': (18, 20, int),          # ?Longitude (minutes)
    'LA.-': (21, 22, str),          # [+-]? Latitude sign
    'LA.d': (22, 24, int),          # ?Latitude (degrees)
    'w_LA': (24, 25, str),          # [*]? Warning about latitude
    'LA.m': (25, 27, int),          # ?Latitude (minutes)
   'w_Mag': (27, 28, str),          # [*]? Warning about magnitude
     'Mag': (28, 31, str),          # Magnitude or magnitude range
}

CROSS_FIELDS = {
    'PNo' : (0, 4, int),            # [1/1028]? Unique star number
    'PCon': (5, 8, str),            # ?Ptolemy constellation
    'PInf': (8, 9, str),            # [~]? ~ if 'informis'
    'PNum': (9, 11, int),           # ?Ptolemy number in constellation

    'NoId': (11, 12, str),          # [*]? Identification issue

    'BCon': (12, 15, str),          # ?Bayer constellation
   'w_Bay': (15, 16, str),          # [*+]? Warning about Bayer designation
    'BLet': (16, 19, str),          # ?Bayer letter in constellation
    'BInd': (20, 21, int),          # ?Bayer index

    'FCon': (22, 25, str),          # ?Flamsteed constellation
  'w_Flm' : (25, 26, str),          # [*+]? Warning about Flamsteed designation
    'FNum': (26, 29, int),          # ?Flamsteed number in constellation

    'ZRa' : (30, 32, int),          # [0/23]? Piazzi right ascension wedge
    'ZNo' : (33, 36, int),          # ?Piazzi number within right ascension wedge

    'LNum': (37, 41, int),          # [0/1942]? Lacaille number

    'HR'  : (42, 46, int),          # [0/9110]? HR (Bright Star) or Ambronn number
  'w_HR'  : (46, 47, str),          # [*+]? Warning about the HR or Ambronn number
}

GREEK_LETTERS = {
    'alp': 'α',
    'bet': 'β',
    'gam': 'γ',
    'del': 'δ',
    'eps': 'ε',
    'zet': 'ζ',
    'eta': 'η',
    'the': 'θ',
    'iot': 'ι',
    'kap': 'κ',
    'lam': 'λ',
    'mu': 'μ',
    'nu': 'ν',
    'xi': 'ξ',
    'omi': 'ο',
    'pi': 'π',
    'rho': 'ρ',
    'sig': 'σ',
    'tau': 'τ',
    'ups': 'υ',
    'phi': 'φ',
    'chi': 'χ',
    'psi': 'ψ',
    'ome': 'ω',
}

def parse_dat(schema):
    def parse(path):
        with open(path) as f:
            for line in f:
                row = {}
                for field, (b, e, t) in schema.items():
                    value = line[b:e].strip()
                    if value:
                        row[field] = t(value)
                yield row
    return parse

parse_cross = parse_dat(CROSS_FIELDS)
parse_cat = parse_dat(CAT_FIELDS)

def parse_names(path):
    with open(path) as f:
        for line in f:
            hip, name = line.strip().split('|')
            yield int(hip), name

HIP = 0
HR = 4
def parse_cross_id(path):
    hr_to_hip = {}
    with open(path) as f:
        next(f, None)   # skip header line
        for line in f:
            parts = line.split('\t')
            hip = int(parts[HIP])
            hr = parts[HR].strip()
            if hr:
                hr_to_hip.setdefault(int(hr), []).append(hip)
    return hr_to_hip

a = list(parse_cat('ptolemy/ptolemy_t.dat'))
c = list(parse_cross('ptolemy/cross_t.dat'))

# Count identifiers is cross
def count_identifiers(path):
    c = Counter()
    for d in parse_cross(path):
        for f in ['BCon', 'FCon', 'ZRa', 'LNum', 'HR']:
            if f in d:
                c[f] += 1
    return c

def make_name(d):
    # if d['PNo'] == 14: breakpoint()
    bl = GREEK_LETTERS.get(d.get('BLet'))
    if bl is not None:
        bi = d.get('BInd', '')
        return f"{bl}{bi}_{d['BCon']}"
    fn = d.get('FNum')
    if fn is not None:
        return f"{fn}_{d['FCon']}"
    hr = d.get('HR')
    if hr is not None:
        return f"HR {hr}"
    #breakpoint()
    return f"{d['PCon']}{d.get('PInf', ' ')}{d['PNum']}"

def find_hip_numbers(cross_path, names_path):
    hr_to_hip = parse_cross_id(CROSS_ID)
    idx_to_hip = {}
    name_to_hip = {name: hip for hip, name in parse_names(names_path)}
    for d in parse_cross(cross_path):
        idx = d.get('PNo')
        if idx is None:
            continue
        name = make_name(d)
        hip = name_to_hip.get(name)
        if hip is None:
            # try alternative names
            bl = d.get('BLet', '')
            name2 = GREEK_LETTERS.get(bl, '') + '1_' + d.get('BCon', '')
            hip = (
                name_to_hip.get(name2) or
                name_to_hip.get(name2 + '_A') or
                name_to_hip.get(name + '_A'))
        if hip is None:
            hr = d.get('HR')
            if hr is not None:
                hip = hr_to_hip.get(hr)
        if hip is not None:
            idx_to_hip[idx] = hip
        else:
            print(f"No HIP found for {name}.")
    return idx_to_hip

counts = count_identifiers('ptolemy/cross_t.dat')
print(counts)
idx_to_hip = find_hip_numbers('ptolemy/cross_t.dat', NAMES_PATH)