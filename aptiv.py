import requests


request = {
    "ClientData": {
        "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
        "VisitId": None,
        "VisitorId": None,
        "Custom": {"custom": None}
    },
    "Keyword": "",
    "FacetSelections": {},
    "PageNo": 0,
    "IndexName": "",
    "IgnoreSpellcheck": False,
    "IsInPreview": True,
    "ClientGuid": "425f6702e15a49298831856bdfdfc6ea",
    "Is100CoverageTurnedOn": False,
    "Query": '',
    "CustomUrl": ''
}


def build_request(page_no):
    request['PageNo'] = page_no
    return request


request = build_request(0)

response = requests.post('https://aptivcatalog.searchapi-na.hawksearch.com/api/v2/search/', json=request)

data = response.json()

import json

with open('facets.json', 'w') as f:
    f.write(json.dumps(data['Facets'], indent=4))

options = {}

page_count = data['Pagination']['NofPages']

import time

results = []

for result in data['Results']:
    results.append(result['Document'])

result_count = 0

for i in range(1, page_count):
    print(i, '...', page_count)
    time.sleep(0.01)
    request = build_request(i)

    response = requests.post(
        'https://aptivcatalog.searchapi-na.hawksearch.com/api/v2/search/',
        json=request
    )

    data = response.json()
    for result in data['Results']:
        results.append(result['Document'])

import os

connectors = []
seals = []
terminals = []
unknown = []
accessories = []
hv_interconnects = []
pin_headers = []
high_voltage_charging = []
srs = []
high_speed = []
covers = []
boots = []


part_types = set()

for result in results:
    part_types.add(('itemcomponenttype_en', tuple(result.get('itemcomponenttype_en', ['None']))))
    part_types.add(('productseriesproductline_en', tuple(result.get('productseriesproductline_en', ['None']))))
    part_types.add(('channelnodeproducts_en', tuple(result.get('channelnodeproducts_en', ['None']))))
    part_types.add(('itemdrmproductfamily_en', tuple(result.get('itemdrmproductfamily_en', ['None']))))

    if 'productseriesproductline_en' in result:
        type = result['productseriesproductline_en']
        for t in type:
            if t == 'Terminals':
                terminals.append(result)
                break
            if t == 'Connectors':
                connectors.append(result)
                break
            if t == 'Accessories':
                if 'itemcomponenttype_en' in result:
                    types = result['itemcomponenttype_en']

                    if 'CONNECTOR' in types:
                        connectors.append(result)
                        break

                    if 'COVER' in types:
                        covers.append(result)
                        break

                    if 'SEAL' in types:
                        seals.append(result)
                        break

                    if 'TERMINAL' in types:
                        terminals.append(result)
                        break

                    if 'LOCKING DEVICE' in types:
                        accessories.append(result)
                        break
                    if 'SLEEVE / BOOT' in types:
                        boots.append(result)
                        break
                elif 'channelnodeproducts_en' in result:
                    types = result['channelnodeproducts_en']

                    if (
                        'CONNECTORS' in types or
                        'SRS' in types or
                        'MEPAPINHEADER' in types or
                        'HVINTERCONNECTS' in types or
                        'HVCHARGING' in types or
                        'HSCA' in types
                    ):
                        connectors.append(result)
                        break

                    if 'SEALS' in types:
                        seals.append(result)
                        break

                    if 'TERMINALS' in types:
                        terminals.append(result)
                        break

                break
            if t == 'NCB (Seals)':
                seals.append(result)
                break
            if t == 'HV Interconnects':
                connectors.append(result)
                break
            if t == 'MepaPinheader':
                connectors.append(result)
                break
            if t == 'HSCA':
                connectors.append(result)
                break
            if t == 'HV Charging':
                connectors.append(result)
                break
            if t == 'SRS':
                connectors.append(result)
                break

        else:
            unknown.append(result)


connectors_fields = dict()
seals_fields = dict()
terminals_fields = dict()
accessories_fields = dict()
hv_interconnects_fields = dict()
pin_headers_fields = dict()
high_voltage_charging_fields = dict()
srs_fields = dict()
high_speed_fields = dict()
covers_fields = dict()
boots_fields = dict()


all_fields = set()


color_data = (
    (0, 'Black', 0x000000),
    (1, 'Brown', 0x8C7355),
    (2, 'Red', 0xFE0000),
    (3, 'Orange', 0xFFA500),
    (4, 'Yellow', 0xFFFF01),
    (5, 'Green', 0x28C629),
    (6, 'Blue', 0x0000FE),
    (7, 'Violet', 0x9400D4),
    (8, 'Gray', 0xA1A1A1),
    (9, 'White', 0xFFFFFF),
    (10, 'Absolute Zero', 0x0048BA),
    (11, 'Acid Green', 0xB0BF1A),
    (12, 'Alice Blue', 0xF0F8FF),
    (13, 'Alizarin crimson', 0xE32636),
    (14, 'Amaranth', 0xE52B50),
    (15, 'Amber', 0xFFBF00),
    (16, 'Amethyst', 0x9966CC),
    (17, 'Antique White', 0xFAEBD7),
    (18, 'Antique White1', 0xFFEFDB),
    (19, 'Antique White2', 0xEEDFCC),
    (20, 'Antique White3', 0xCDC0B0),
    (21, 'Antique White4', 0x8B8378),
    (22, 'Apricot', 0xFBCEB1),
    (23, 'Aqua', 0x00FFFF),
    (24, 'Aquamarine1', 0x7FFFD4),
    (25, 'Aquamarine2', 0x76EEC6),
    (26, 'Aquamarine4', 0x458B74),
    (27, 'Army Green', 0x4B5320),
    (28, 'Arylide Yellow', 0xE9D66B),
    (29, 'Ash Grey', 0xB2BEB5),
    (30, 'Asparagus', 0x87A96B),
    (31, 'Aureolin', 0xFDEE00),
    (32, 'Azure1', 0xF0FFFF),
    (33, 'Azure2', 0xE0EEEE),
    (34, 'Azure3', 0xC1CDCD),
    (35, 'Azure4', 0x838B8B),
    (36, 'Baby Blue', 0x89CFF0),
    (37, 'Baby Pink', 0xF4C2C2),
    (38, 'Baker-Miller Pink', 0xFF91AF),
    (39, 'Banana Mania', 0xFAE7B5),
    (40, 'Banana Yellow', 0xFFE135),
    (41, 'Barn Red', 0x7C0A02),
    (42, 'Battleship Gray', 0x848482),
    (43, 'Beaver', 0x9F8170),
    (44, 'Beige', 0xF5F5DC),
    (45, 'Bisque1', 0xFFE4C4),
    (46, 'Bisque2', 0xEED5B7),
    (47, 'Bisque3', 0xCDB79E),
    (48, 'Bisque4', 0x8B7D6B),
    (49, 'Bistre', 0x3D2B1F),
    (50, 'Bitter Lemon', 0xCAE00D),
    (51, 'Bitter Lime', 0xBFFF00),
    (52, 'Bittersweet', 0xFE6F5E),
    (53, 'Bittersweet Shimmer', 0xBF4F51),
    (54, 'Black Coffee', 0x3B2F2F),
    (55, 'Black Olive', 0x3B3C36),
    (56, 'Black Shadows', 0xBFAFB2),
    (57, 'Blanched Almond', 0xFFEBCD),
    (58, 'Bleu de France', 0x318CE7),
    (59, 'Blond', 0xFAF0BE),
    (60, 'Blue (Pantone)', 0x0018A8),
    (61, 'Blue Bell', 0xA2A2D0),
    (62, 'Blue Green', 0x0D98BA),
    (63, 'Blue1', 0x0000FF),
    (64, 'Blue2', 0x0000EE),
    (65, 'Dark Blue', 0x00008B),
    (66, 'Blue Violet', 0x8A2BE2),
    (67, 'Bole', 0x79443B),
    (68, 'Bone', 0xE3DAC9),
    (69, 'Boysenberry', 0x873260),
    (70, 'Brandeis Blue', 0x0070FF),
    (71, 'Brass', 0xB5A642),
    (72, 'Brick Red', 0xCB4154),
    (73, 'Bright Cerulean', 0x1DACD6),
    (74, 'Bright Green', 0x66FF00),
    (75, 'Bright Lavender', 0xBF94E4),
    (76, 'Bright Lilac', 0xD891EF),
    (77, 'Bright Maroon', 0xC32148),
    (78, 'Bright Navy Blue', 0x1974D2),
    (79, 'Bright Turquoise', 0x08E8DE),
    (80, 'Bright Ube', 0xD19FE8),
    (81, 'Brilliant Rose', 0xFF55A3),
    (82, 'Brink Pink', 0xFB607F),
    (83, 'British Racing Green', 0x004225),
    (84, 'Bronze', 0xCD7F32),
    (85, 'Brown1', 0xFF4040),
    (86, 'Brown2', 0xEE3B3B),
    (87, 'Brown3', 0xCD3333),
    (88, 'Brown4', 0x8B2323),
    (89, 'Brunswick Green', 0x1B4D3E),
    (90, 'Bubble Gum', 0xFFC1CC),
    (91, 'Buff', 0xF0DC82),
    (92, 'Bulgarian Rose', 0x480607),
    (93, 'Burgundy', 0x800020),
    (94, 'Burlywood', 0xDEB887),
    (95, 'Burlywood1', 0xFFD39B),
    (96, 'Burlywood2', 0xEEC591),
    (97, 'Burlywood3', 0xCDAA7D),
    (98, 'Burlywood4', 0x8B7355),
    (99, 'Burnished Brown', 0xA17A74),
    (100, 'Burnt Orange', 0xCC5500),
    (101, 'Burnt Sienna', 0xE97451),
    (102, 'Burnt Umber', 0x8A3324),
    (103, 'Byzantine', 0xBD33A4),
    (104, 'Byzantium', 0x702963),
    (105, 'Cadet Grey', 0x91A3B0),
    (106, 'Cadet Blue', 0x5F9EA0),
    (107, 'Cadet Blue1', 0x98F5FF),
    (108, 'Cadet Blue2', 0x8EE5EE),
    (109, 'Cadet Blue3', 0x7AC5CD),
    (110, 'Cadet Blue4', 0x53868B),
    (111, 'Cadmium Green', 0x006B3C),
    (112, 'Cadmium Orange', 0xED872D),
    (113, 'Cadmium Red', 0xE30022),
    (114, 'Cadmium Yellow', 0xFFF600),
    (115, 'Cambridge Blue', 0xA3C1AD),
    (116, 'Camel', 0xC19A6B),
    (117, 'Cameo Pink', 0xEFBBCC),
    (118, 'Camouflage Green', 0x78866B),
    (119, 'Canary', 0xFFFF99),
    (120, 'Canary Yellow', 0xFFEF00),
    (121, 'Candy Apple Red', 0xFF0800),
    (122, 'Candy Pink', 0xE4717A),
    (123, 'Caput Mortuum', 0x592720),
    (124, 'Cardinal', 0xC41E3A),
    (125, 'Caribbean Green', 0x00CC99),
    (126, 'Carmine', 0x960018),
    (127, 'Carmine Pink', 0xEB4C42),
    (128, 'Carnation Pink', 0xFFA6C9),
    (129, 'Carnelian', 0xB31B1B),
    (130, 'Carolina Blue', 0x56A0D3),
    (131, 'Carrot Orange', 0xED9121),
    (132, 'Castleton Green', 0x00563F),
    (133, 'Cedar Chest', 0xC95A49),
    (134, 'Celadon', 0xACE1AF),
    (135, 'Celadon Green', 0x2F847C),
    (136, 'Celeste', 0xB2FFFF),
    (137, 'Celtic Blue', 0x246BCE),
    (138, 'Cerise', 0xDE3163),
    (139, 'Cerulean', 0x007BA7),
    (140, 'Cerulean Blue', 0x2A52BE),
    (141, 'Cerulean Frost', 0x6D9BC3),
    (142, 'Cg Blue', 0x007AA5),
    (143, 'Chamoisee', 0xA0785A),
    (144, 'Champagne', 0xF7E7CE),
    (145, 'Charcoal', 0x36454F),
    (146, 'Chartreuse1', 0x7FFF00),
    (147, 'Chartreuse2', 0x76EE00),
    (148, 'Chartreuse3', 0x66CD00),
    (149, 'Chartreuse4', 0x458B00),
    (150, 'Cherry Blossom Pink', 0xFFB7C5),
    (151, 'Chestnut', 0x954535),
    (152, 'Chocolate', 0xD2691E),
    (153, 'Chocolate1', 0xFF7F24),
    (154, 'Chocolate2', 0xEE7621),
    (155, 'Chocolate3', 0xCD661D),
    (156, 'Chrome Yellow', 0xFFA700),
    (157, 'Cinereous', 0x98817B),
    (158, 'Cinnabar', 0xE34234),
    (159, 'Citrine', 0xE4D00A),
    (160, 'Citron', 0x9FA91F),
    (161, 'Claret', 0x7F1734),
    (162, 'Cobalt', 0x0047AB),
    (163, 'Coffee', 0x6F4E37),
    (164, 'Cool Grey', 0x8C92AC),
    (165, 'Copper', 0xB87333),
    (166, 'Copper Red', 0xCB6D51),
    (167, 'Copper Rose', 0x996666),
    (168, 'Coquelicot', 0xFF3800),
    (169, 'Coral', 0xFF7F50),
    (170, 'Coral Pink', 0xF88379),
    (171, 'Coral1', 0xFF7256),
    (172, 'Coral2', 0xEE6A50),
    (173, 'Coral3', 0xCD5B45),
    (174, 'Coral4', 0x8B3E2F),
    (175, 'Cordovan', 0x893F45),
    (176, 'Corn', 0xFBEC5D),
    (177, 'Cornflower Blue', 0x6495ED),
    (178, 'Cornsilk', 0xFFF8DC),
    (179, 'Cornsilk1', 0xEEE8CD),
    (180, 'Cornsilk2', 0xCDC8B1),
    (181, 'Cornsilk3', 0x8B8878),
    (182, 'Cosmic Cobalt', 0x2E2D88),
    (183, 'Cosmic Latte', 0xFFF8E7),
    (184, 'Cotton Candy', 0xFFBCD9),
    (185, 'Cream', 0xFFFDD0),
    (186, 'Crimson', 0xDC143C),
    (187, 'Crystal', 0xA7D8DE),
    (188, 'Cyan1', 0x00FFFF),
    (189, 'Cyan2', 0x00EEEE),
    (190, 'Cyan3', 0x00CDCD),
    (191, 'Cyan4', 0x008B8B),
    (192, 'Cyclamen', 0xF56FA1),
    (193, 'Daffodil', 0xFFFF31),
    (194, 'Dandelion', 0xF0E130),
    (195, 'Dark Brown', 0x654321),
    (196, 'Dark Byzantium', 0x5D3954),
    (197, 'Dark Jungle Green', 0x1A2421),
    (198, 'Dark Lavender', 0x734F96),
    (199, 'Dark Moss Green', 0x4A5D23),
    (200, 'Dark Pastel Green', 0x03C03C),
    (201, 'Dark Sienna', 0x3C1414),
    (202, 'Dark Sky Blue', 0x8CBED6),
    (203, 'Dark Spring Green', 0x177245),
    (204, 'Dark Goldenrod', 0xB8860B),
    (205, 'Dark Goldenrod1', 0xFFB90F),
    (206, 'Dark Goldenrod2', 0xEEAD0E),
    (207, 'Dark Goldenrod3', 0xCD950C),
    (208, 'Dark Goldenrod4', 0x8B6508),
    (209, 'Dark Green', 0x006400),
    (210, 'Dark Khaki', 0xBDB76B),
    (211, 'Dark Olive Green', 0x556B2F),
    (212, 'Dark Olive Green1', 0xCAFF70),
    (213, 'Dark Olive Green2', 0xBCEE68),
    (214, 'Dark Olive Green3', 0xA2CD5A),
    (215, 'Dark Olive Green4', 0x6E8B3D),
    (216, 'Dark Orange', 0xFF8C00),
    (217, 'Dark Orange1', 0xFF7F00),
    (218, 'Dark Orange2', 0xEE7600),
    (219, 'Dark Orange3', 0xCD6600),
    (220, 'Dark Orange4', 0x8B4500),
    (221, 'Dark Orchid', 0x9932CC),
    (222, 'Dark Orchid1', 0xBF3EFF),
    (223, 'Dark Orchid2', 0xB23AEE),
    (224, 'Dark Orchid3', 0x9A32CD),
    (225, 'Dark Orchid4', 0x68228B),
    (226, 'Dark Salmon', 0xE9967A),
    (227, 'Dark Sea Green', 0x8FBC8F),
    (228, 'Dark Sea Green1', 0xC1FFC1),
    (229, 'Dark Sea Green2', 0xB4EEB4),
    (230, 'Dark Sea Green3', 0x9BCD9B),
    (231, 'Dark Sea Green4', 0x698B69),
    (232, 'Dark Slate Blue', 0x483D8B),
    (233, 'Dark Slate Gray', 0x2F4F4F),
    (234, 'Dark Slate Gray1', 0x97FFFF),
    (235, 'Dark Slate Gray2', 0x8DEEEE),
    (236, 'Dark Slate Gray3', 0x79CDCD),
    (237, 'Dark Slate Gray4', 0x528B8B),
    (238, 'Dark Turquoise', 0x00CED1),
    (239, 'Dark Violet', 0x9400D3),
    (240, 'Dartmouth Green', 0x00703C),
    (241, 'Deep Cerise', 0xDA3287),
    (242, 'Deep Champagne', 0xFAD6A5),
    (243, 'Deep Fuchsia', 0xC154C1),
    (244, 'Deep Jungle Green', 0x004B49),
    (245, 'Deep Peach', 0xFFCBA4),
    (246, 'Deep Saffron', 0xFF9933),
    (247, 'Deep Space Sparkle', 0x4A646C),
    (248, 'Deep chestnut', 0xB94E48),
    (249, 'Deep Pink', 0xFF1493),
    (250, 'Deep Pink1', 0xEE1289),
    (251, 'Deep Pink2', 0xCD1076),
    (252, 'Deep Pink3', 0x8B0A50),
    (253, 'Deep Sky Blue', 0x00BFFF),
    (254, 'Deep Sky Blue1', 0x00B2EE),
    (255, 'Deep Sky Blue2', 0x009ACD),
    (256, 'Deep Sky Blue3', 0x00688B),
    (257, 'Denim', 0x1560BD),
    (258, 'Denim Blue', 0x2243B6),
    (259, 'Desert Sand', 0xEDC9AF),
    (260, 'Dim Gray', 0x696969),
    (261, 'Dodger Blue1', 0x1E90FF),
    (262, 'Dodger Blue2', 0x1C86EE),
    (263, 'Dodger Blue3', 0x1874CD),
    (264, 'Dodger Blue4', 0x104E8B),
    (265, 'Dogwood Rose', 0xD71868),
    (266, 'Dutch White', 0xEFDFBB),
    (267, 'Earth Yellow', 0xE1A95F),
    (268, 'Ebony', 0x555D50),
    (269, 'Eggplant', 0x614051),
    (270, 'Eggshell', 0xF0EAD6),
    (271, 'Egyptian Blue', 0x1034A6),
    (272, 'Electric Blue', 0x7DF9FF),
    (273, 'Electric Indigo', 0x6F00FF),
    (274, 'Electric Lime', 0xCCFF00),
    (275, 'Electric Purple', 0xBF00FF),
    (276, 'Emerald', 0x50C878),
    (277, 'Eminence', 0x6C3082),
    (278, 'Eton Blue', 0x96C8A2),
    (279, 'Falu Red', 0x801818),
    (280, 'Fawn', 0xE5AA70),
    (281, 'Feldgrau', 0x4D5D53),
    (282, 'Fern Green', 0x4F7942),
    (283, 'Ferrari Red', 0xFF2800),
    (284, 'Fire Opal', 0xE95C4B),
    (285, 'Firebrick', 0xB22222),
    (286, 'Firebrick1', 0xFF3030),
    (287, 'Firebrick2', 0xEE2C2C),
    (288, 'Firebrick3', 0xCD2626),
    (289, 'Firebrick4', 0x8B1A1A),
    (290, 'Flamingo Pink', 0xFC8EAC),
    (291, 'Floral White', 0xFFFAF0),
    (292, 'Flourescent Blue', 0x15F4EE),
    (293, 'Forest Green', 0x228B22),
    (294, 'Forest Green1', 0x228B22),
    (295, 'French Beige', 0xA67B5B),
    (296, 'French Bistre', 0x856D4D),
    (297, 'French Blue', 0x0072BB),
    (298, 'French Lilac', 0x86608E),
    (299, 'French Mauve', 0xD473D4),
    (300, 'French Pink', 0xFD6C9E),
    (301, 'French Rose', 0xF64A8A),
    (302, 'French Sky Blue', 0x77B5FE),
    (303, 'French Violet', 0x8806CE),
    (304, 'Frostbite', 0xE936A7),
    (305, 'Fuchsia Purple', 0xCC397B),
    (306, 'Fuchsia Rose', 0xC74375),
    (307, 'Fulvous', 0xE48400),
    (308, 'Fuzzy Wuzzy', 0x87421F),
    (309, 'GO Green', 0x00AB66),
    (310, 'Gainsboro', 0xDCDCDC),
    (311, 'Gamboge', 0xE49B0F),
    (312, 'Generic Viridian', 0x007F66),
    (313, 'Ghost White', 0xF8F8FF),
    (314, 'Ginger', 0xB06500),
    (315, 'Glaucous', 0x6082B6),
    (316, 'Glossy Grape', 0xAB92B3),
    (317, 'Gold Fusion', 0x85754E),
    (318, 'Gold1', 0xFFD700),
    (319, 'Gold2', 0xEEC900),
    (320, 'Gold3', 0xCDAD00),
    (321, 'Gold4', 0x8B7500),
    (322, 'Golden Brown', 0x996515),
    (323, 'Golden Poppy', 0xFCC200),
    (324, 'Golden Yellow', 0xFFDF00),
    (325, 'Goldenrod', 0xDAA520),
    (326, 'Goldenrod1', 0xFFC125),
    (327, 'Goldenrod2', 0xEEB422),
    (328, 'Goldenrod3', 0xCD9B1D),
    (329, 'Goldenrod4', 0x8B6914),
    (330, 'Granite Gray', 0x676767),
    (331, 'Granny Smith Apple', 0xA8E4A0),
    (332, 'Gray1', 0x030303),
    (333, 'Gray10', 0x1A1A1A),
    (334, 'Gray11', 0x1C1C1C),
    (335, 'Gray12', 0x1F1F1F),
    (336, 'Gray13', 0x212121),
    (337, 'Gray14', 0x242424),
    (338, 'Gray15', 0x262626),
    (339, 'Gray16', 0x292929),
    (340, 'Gray17', 0x2B2B2B),
    (341, 'Gray18', 0x2E2E2E),
    (342, 'Gray19', 0x303030),
    (343, 'Gray2', 0x050505),
    (344, 'Gray20', 0x333333),
    (345, 'Gray21', 0x363636),
    (346, 'Gray22', 0x383838),
    (347, 'Gray23', 0x3B3B3B),
    (348, 'Gray24', 0x3D3D3D),
    (349, 'Gray25', 0x404040),
    (350, 'Gray26', 0x424242),
    (351, 'Gray27', 0x454545),
    (352, 'Gray28', 0x474747),
    (353, 'Gray29', 0x4A4A4A),
    (354, 'Gray3', 0x080808),
    (355, 'Gray30', 0x4D4D4D),
    (356, 'Gray31', 0x4F4F4F),
    (357, 'Gray32', 0x525252),
    (358, 'Gray33', 0x545454),
    (359, 'Gray34', 0x575757),
    (360, 'Gray35', 0x595959),
    (361, 'Gray36', 0x5C5C5C),
    (362, 'Gray37', 0x5E5E5E),
    (363, 'Gray38', 0x616161),
    (364, 'Dark Gray', 0x636363),
    (365, 'Jet Black', 0x0A0A0A),
    (366, 'Gray40', 0x666666),
    (367, 'Gray41', 0x696969),
    (368, 'Gray42', 0x6B6B6B),
    (369, 'Gray43', 0x6E6E6E),
    (370, 'Gray44', 0x707070),
    (371, 'Gray45', 0x737373),
    (372, 'Gray46', 0x757575),
    (373, 'Gray47', 0x787878),
    (374, 'Gray48', 0x7A7A7A),
    (375, 'Gray49', 0x7D7D7D),
    (376, 'Gray5', 0x0D0D0D),
    (377, 'Gray50', 0x7F7F7F),
    (378, 'Gray51', 0x828282),
    (379, 'Gray52', 0x858585),
    (380, 'Gray53', 0x878787),
    (381, 'Gray54', 0x8A8A8A),
    (382, 'Gray55', 0x8C8C8C),
    (383, 'Gray56', 0x8F8F8F),
    (384, 'Gray57', 0x919191),
    (385, 'Gray58', 0x949494),
    (386, 'Gray59', 0x969696),
    (387, 'Gray6', 0x0F0F0F),
    (388, 'Gray60', 0x999999),
    (389, 'Gray61', 0x9C9C9C),
    (390, 'Gray62', 0x9E9E9E),
    (391, 'Gray63', 0xA1A1A1),
    (392, 'Gray64', 0xA3A3A3),
    (393, 'Gray65', 0xA6A6A6),
    (394, 'Gray66', 0xA8A8A8),
    (395, 'Gray67', 0xABABAB),
    (396, 'Gray68', 0xADADAD),
    (397, 'Gray69', 0xB0B0B0),
    (398, 'Gray7', 0x121212),
    (399, 'Gray70', 0xB3B3B3),
    (400, 'Gray71', 0xB5B5B5),
    (401, 'Gray72', 0xB8B8B8),
    (402, 'Gray73', 0xBABABA),
    (403, 'Gray74', 0xBDBDBD),
    (404, 'Gray75', 0xBFBFBF),
    (405, 'Gray76', 0xC2C2C2),
    (406, 'Gray77', 0xC4C4C4),
    (407, 'Gray78', 0xC7C7C7),
    (408, 'Gray79', 0xC9C9C9),
    (409, 'Gray8', 0x141414),
    (410, 'Gray80', 0xCCCCCC),
    (411, 'Gray81', 0xCFCFCF),
    (412, 'Gray82', 0xD1D1D1),
    (413, 'Gray83', 0xD4D4D4),
    (414, 'Gray84', 0xD6D6D6),
    (415, 'Gray85', 0xD9D9D9),
    (416, 'Gray86', 0xDBDBDB),
    (417, 'Gray87', 0xDEDEDE),
    (418, 'Gray88', 0xE0E0E0),
    (419, 'Gray89', 0xE3E3E3),
    (420, 'Gray9', 0x171717),
    (421, 'Gray90', 0xE5E5E5),
    (422, 'Gray91', 0xE8E8E8),
    (423, 'Gray92', 0xEBEBEB),
    (424, 'Gray93', 0xEDEDED),
    (425, 'Gray94', 0xF0F0F0),
    (426, 'Gray95', 0xF2F2F2),
    (427, 'Gray97', 0xF7F7F7),
    (428, 'Gray98', 0xFAFAFA),
    (429, 'Gray99', 0xFCFCFC),
    (430, 'Green (Crayola)', 0x1CAC78),
    (431, 'Green (Pantone)', 0x00AD43),
    (432, 'Green (Pigment)', 0x00A550),
    (433, 'Green Lizard', 0xA7F432),
    (434, 'Green Sheen', 0x6EAEA1),
    (435, 'Green1', 0x00FF00),
    (436, 'Green2', 0x00EE00),
    (437, 'Green3', 0x00CD00),
    (438, 'Green4', 0x008B00),
    (439, 'Green Yellow', 0xADFF2F),
    (440, 'Grullo', 0xA99A86),
    (441, 'Gunmetal', 0x2A3439),
    (442, 'Han Blue', 0x446CCF),
    (443, 'Han Purple', 0x5218FA),
    (444, 'Harlequin', 0x3FFF00),
    (445, 'Harvest Gold', 0xDA9100),
    (446, 'Heliotrope', 0xDF73FF),
    (447, 'Hollywood Cerise', 0xF400A1),
    (448, 'Honeydew1', 0xF0FFF0),
    (449, 'Honeydew2', 0xE0EEE0),
    (450, 'Honeydew3', 0xC1CDC1),
    (451, 'Honeydew4', 0x838B83),
    (452, 'Honolulu Blue', 0x006DB0),
    (453, 'Hot Magenta', 0xFF1DCE),
    (454, 'Hot Pink', 0xFF69B4),
    (455, 'Hot Pink1', 0xFF6EB4),
    (456, 'Hot Pink2', 0xEE6AA7),
    (457, 'Hot Pink3', 0xCD6090),
    (458, 'Hot Pink4', 0x8B3A62),
    (459, 'Hunter Green', 0x355E3B),
    (460, 'Iceberg', 0x71A6D2),
    (461, 'Icterine', 0xFCF75E),
    (462, 'Illuminating Emerald', 0x319177),
    (463, 'Imperial Red', 0xED2939),
    (464, 'Inchworm', 0xB2EC5D),
    (465, 'India Green', 0x138808),
    (466, 'Indian Yellow', 0xE3A857),
    (467, 'Indian Red', 0xCD5C5C),
    (468, 'Indian Red1', 0xFF6A6A),
    (469, 'Indian Red2', 0xEE6363),
    (470, 'Indian Red3', 0xCD5555),
    (471, 'Indian Red4', 0x8B3A3A),
    (472, 'Indigo', 0x4B0082),
    (473, 'International Orange', 0xFF4F00),
    (474, 'Iris', 0x5A4FCF),
    (475, 'Isabelline', 0xF4F0EC),
    (476, 'Ivory1', 0xFFFFF0),
    (477, 'Ivory2', 0xEEEEE0),
    (478, 'Ivory3', 0xCDCDC1),
    (479, 'Ivory4', 0x8B8B83),
    (480, 'Jade', 0x00A86B),
    (481, 'Japanese Carmine', 0x9D2933),
    (482, 'Jasmine', 0xF8DE7E),
    (483, 'Jazzberry Jam', 0xA50B5E),
    (484, 'Jonquil', 0xF4CA16),
    (485, 'Jungle Green', 0x29AB87),
    (486, 'Kelly Green', 0x4CBB17),
    (487, 'Keppel', 0x3AB09E),
    (488, 'Key Lime', 0xE8F48C),
    (489, 'Khaki', 0xF0E68C),
    (490, 'Khaki1', 0xFFF68F),
    (491, 'Khaki2', 0xEEE685),
    (492, 'Khaki3', 0xCDC673),
    (493, 'Khaki4', 0x8B864E),
    (494, 'Kombu Green', 0x354230),
    (495, 'Languid Lavender', 0xD6CADD),
    (496, 'Lapis Lazuli', 0x26619C),
    (497, 'Laser Lemon', 0xFFFF66),
    (498, 'Laurel Green', 0xA9BA9D),
    (499, 'Lavender', 0xE6E6FA),
    (500, 'Lavender (Floral)', 0xB57EDC),
    (501, 'Lavender Blue', 0xCCCCFF),
    (502, 'Lavender Gray', 0xC4C3D0),
    (503, 'Lavender Blush1', 0xFFF0F5),
    (504, 'Lavender Blush2', 0xEEE0E5),
    (505, 'Lavender Blush3', 0xCDC1C5),
    (506, 'Lavender Blush4', 0x8B8386),
    (507, 'Lawn Green', 0x7CFC00),
    (508, 'Lemon', 0xFFF700),
    (509, 'Lemon Curry', 0xCCA01D),
    (510, 'Lemon Glacier', 0xFDFF00),
    (511, 'Lemon Meringue', 0xF6EABE),
    (512, 'Lemon Yellow', 0xFFF44F),
    (513, 'Lemon Chiffon1', 0xFFFACD),
    (514, 'Lemon Chiffon2', 0xEEE9BF),
    (515, 'Lemon Chiffon3', 0xCDC9A5),
    (516, 'Lemon Chiffon4', 0x8B8970),
    (517, 'Light', 0xEEDD82),
    (518, 'Light Cornflower Blue', 0x93CCEA),
    (519, 'Light French Beige', 0xC8AD7F),
    (520, 'Light Orange', 0xFED8B1),
    (521, 'Light Periwinkle', 0xC5CBE1),
    (522, 'Light Blue', 0xADD8E6),
    (523, 'Light Blue1', 0xBFEFFF),
    (524, 'Light Blue2', 0xB2DFEE),
    (525, 'Light Blue3', 0x9AC0CD),
    (526, 'Light Blue4', 0x68838B),
    (527, 'Light Coral', 0xF08080),
    (528, 'Light Cyan1', 0xE0FFFF),
    (529, 'Light Cyan2', 0xD1EEEE),
    (530, 'Light Cyan3', 0xB4CDCD),
    (531, 'Light Cyan4', 0x7A8B8B),
    (532, 'Light Goldenrod1', 0xFFEC8B),
    (533, 'Light Goldenrod2', 0xEEDC82),
    (534, 'Light Goldenrod3', 0xCDBE70),
    (535, 'Light Goldenrod4', 0x8B814C),
    (536, 'Light GoldenrodYellow', 0xFAFAD2),
    (537, 'Light Gray', 0xD3D3D3),
    (538, 'Light Pink', 0xFFB6C1),
    (539, 'Light Pink1', 0xFFAEB9),
    (540, 'Light Pink2', 0xEEA2AD),
    (541, 'Light Pink3', 0xCD8C95),
    (542, 'Light Pink4', 0x8B5F65),
    (543, 'Light Salmon1', 0xFFA07A),
    (544, 'Light Salmon2', 0xEE9572),
    (545, 'Light Salmon3', 0xCD8162),
    (546, 'Light Salmon4', 0x8B5742),
    (547, 'Light SeaGreen', 0x20B2AA),
    (548, 'Light SkyBlue', 0x87CEFA),
    (549, 'Light SkyBlue1', 0xB0E2FF),
    (550, 'Light SkyBlue2', 0xA4D3EE),
    (551, 'Light SkyBlue3', 0x8DB6CD),
    (552, 'Light SkyBlue4', 0x607B8B),
    (553, 'Light SlateBlue', 0x8470FF),
    (554, 'Light SlateGray', 0x778899),
    (555, 'Light SteelBlue', 0xB0C4DE),
    (556, 'Light SteelBlue1', 0xCAE1FF),
    (557, 'Light SteelBlue2', 0xBCD2EE),
    (558, 'Light SteelBlue3', 0xA2B5CD),
    (559, 'Light SteelBlue4', 0x6E7B8B),
    (560, 'Light Yellow1', 0xFFFFE0),
    (561, 'Light Yellow2', 0xEEEED1),
    (562, 'Light Yellow3', 0xCDCDB4),
    (563, 'Light Yellow4', 0x8B8B7A),
    (564, 'Lilac', 0xC8A2C8),
    (565, 'Lilac Luster', 0xAE98AA),
    (566, 'Lime Green', 0x32CD32),
    (567, 'Lincoln Green', 0x195905),
    (568, 'Linen', 0xFAF0E6),
    (569, 'Little Boy Blue', 0x6CA0DC),
    (570, 'MSU Green', 0x18453B),
    (571, 'Macaroni and Cheese', 0xFFBD88),
    (572, 'Madder Lake', 0xCC3336),
    (573, 'Magenta', 0xFF00FF),
    (574, 'Magenta (Crayola)', 0xF653A6),
    (575, 'Magenta (Pantone)', 0xD0417E),
    (576, 'Magenta Haze', 0x9F4576),
    (577, 'Magenta2', 0xEE00EE),
    (578, 'Magenta3', 0xCD00CD),
    (579, 'Magenta4', 0x8B008B),
    (580, 'Magic Mint', 0xAAF0D1),
    (581, 'Mahogany', 0xC04000),
    (582, 'Majorelle Blue', 0x6050DC),
    (583, 'Malachite', 0x0BDA51),
    (584, 'Manatee', 0x979AAA),
    (585, 'Mandarin', 0xF37A48),
    (586, 'Mango', 0xFDBE02),
    (587, 'Mango Tango', 0xFF8243),
    (588, 'Mantis', 0x74C365),
    (589, 'Marigold', 0xEAA221),
    (590, 'Maroon', 0xB03060),
    (591, 'Maroon1', 0xFF34B3),
    (592, 'Maroon2', 0xEE30A7),
    (593, 'Maroon3', 0xCD2990),
    (594, 'Maroon4', 0x8B1C62),
    (595, 'Mauve', 0xE0B0FF),
    (596, 'Mauve Taupe', 0x915F6D),
    (597, 'Mauvelous', 0xEF98AA),
    (598, 'Maximum Blue Green', 0x30BFBF),
    (599, 'Maximum Blue Purple', 0xACACE6),
    (600, 'Maximum Green', 0x5E8C31),
    (601, 'Maximum Blue', 0x47ABCC),
    (602, 'May Green', 0x4C9141),
    (603, 'Maya Blue', 0x73C2FB),
    (604, 'Medium', 0x66CDAA),
    (605, 'Medium Aquamarine', 0x66DDAA),
    (606, 'Medium Candy Apple Red', 0xE2062C),
    (607, 'Medium Carmine', 0xAF4035),
    (608, 'Medium Champagne', 0xF3E5AB),
    (609, 'Medium Aquamarine', 0x66CDAA),
    (610, 'Medium Blue', 0x0000CD),
    (611, 'Medium Orchid', 0xBA55D3),
    (612, 'Medium Orchid1', 0xE066FF),
    (613, 'Medium Orchid2', 0xD15FEE),
    (614, 'Medium Orchid3', 0xB452CD),
    (615, 'Medium Orchid4', 0x7A378B),
    (616, 'Medium Purple', 0x9370DB),
    (617, 'Medium Purple1', 0xAB82FF),
    (618, 'Medium Purple2', 0x9F79EE),
    (619, 'Medium Purple3', 0x8968CD),
    (620, 'Medium Purple4', 0x5D478B),
    (621, 'Medium SeaG reen', 0x3CB371),
    (622, 'Medium Slate Blue', 0x7B68EE),
    (623, 'Medium Spring Green', 0x00FA9A),
    (624, 'Medium Turquoise', 0x48D1CC),
    (625, 'Medium Violet Red', 0xC71585),
    (626, 'Mellow Apricot', 0xF8B878),
    (627, 'Melon', 0xFEBAAD),
    (628, 'Metallic Gold', 0xD3AF37),
    (629, 'Metallic Seaweed', 0x0A7E8C),
    (630, 'Metallic Sunburst', 0x9C7C38),
    (631, 'Mexican Pink', 0xE4007C),
    (632, 'Medium Blue', 0x7ED4E6),
    (633, 'Medium Blue Green', 0x8DD9CC),
    (634, 'Medium Blue Purple', 0x8B72BE),
    (635, 'Medium Green', 0x4D8C57),
    (636, 'Medium Green Yellow', 0xACBF60),
    (637, 'Medium Gray', 0x8B8680),
    (638, 'Medium Purple', 0xD982B5),
    (639, 'Medium Red', 0xE58E73),
    (640, 'Medium Red Purple', 0xA55353),
    (641, 'Medium Yellow', 0xFFEB00),
    (642, 'Medium Yellow Red', 0xECB176),
    (643, 'Midnight Green', 0x004953),
    (644, 'Midnight Blue', 0x191970),
    (645, 'Mikado Yellow', 0xFFC40C),
    (646, 'Mimi Pink', 0xFFDAE9),
    (647, 'Mindaro', 0xE3F988),
    (648, 'Minion Yellow', 0xF5E050),
    (649, 'Mint', 0x3EB489),
    (650, 'Mint Green', 0x98FF98),
    (651, 'Mint Cream', 0xF5FFFA),
    (652, 'Misty Moss', 0xBBB477),
    (653, 'Misty Rose1', 0xFFE4E1),
    (654, 'Misty Rose2', 0xEED5D2),
    (655, 'Misty Rose3', 0xCDB7B5),
    (656, 'Misty Rose4', 0x8B7D7B),
    (657, 'Moccasin', 0xFFE4B5),
    (658, 'Mode Beige', 0x967117),
    (659, 'Moss Green', 0x8A9A5B),
    (660, 'Mountain Meadow', 0x30BA8F),
    (661, 'Mountbatten Pink', 0x997A8D),
    (662, 'Mulberry', 0xC54B8C),
    (663, 'Mustard', 0xFFDB58),
    (664, 'Myrtle Green', 0x317873),
    (665, 'Mystic Maroon', 0xAD4379),
    (666, 'Nadeshiko Pink', 0xF6ADC6),
    (667, 'Navajo White1', 0xFFDEAD),
    (668, 'Navajo White2', 0xEECFA1),
    (669, 'Navajo White3', 0xCDB38B),
    (670, 'Navajo White4', 0x8B795E),
    (671, 'Navy Blue', 0x000080),
    (672, 'Neon Blue', 0x4666FF),
    (673, 'Neon Carrot', 0xFFA343),
    (674, 'Neon Fuchsia', 0xFE4164),
    (675, 'Neon Green', 0x39FF14),
    (676, 'Nickel', 0x727472),
    (677, 'Nyanza', 0xE9FFDB),
    (678, 'Ocean Blue', 0x4F42B5),
    (679, 'Ocean Green', 0x48BF91),
    (680, 'Ochre', 0xCC7722),
    (681, 'Old Burgundy', 0x43302E),
    (682, 'Old Gold', 0xCFB53B),
    (683, 'Old Lavender', 0x796878),
    (684, 'Old Mauve', 0x673147),
    (685, 'Old Rose', 0xC08081),
    (686, 'Old Lace', 0xFDF5E6),
    (687, 'Olive', 0x808000),
    (688, 'Olive Green', 0xB5B35C),
    (689, 'Olive Drab', 0x6B8E23),
    (690, 'Olive Drab1', 0xC0FF3E),
    (691, 'Olive Drab2', 0xB3EE3A),
    (692, 'Olive Drab4', 0x698B22),
    (693, 'Olivine', 0x9AB973),
    (694, 'Opal', 0xA8C3BC),
    (695, 'Opera Maue', 0xB784A7),
    (696, 'Orange (Crayola)', 0xFF5800),
    (697, 'Orange Peel', 0xFF9F00),
    (698, 'Orange Soda', 0xFA5B3D),
    (699, 'Orange1', 0xFFA500),
    (700, 'Orange2', 0xEE9A00),
    (701, 'Orange3', 0xCD8500),
    (702, 'Orange4', 0x8B5A00),
    (703, 'Orange Red1', 0xFF4500),
    (704, 'Orange Red2', 0xEE4000),
    (705, 'Orange Red3', 0xCD3700),
    (706, 'Orange Red4', 0x8B2500),
    (707, 'Orchid', 0xDA70D6),
    (708, 'Orchid (Crayola)', 0xE29CD2),
    (709, 'Orchid Pink', 0xF2BDCD),
    (710, 'Orchid1', 0xFF83FA),
    (711, 'Orchid2', 0xEE7AE9),
    (712, 'Orchid3', 0xCD69C9),
    (713, 'Orchid4', 0x8B4789),
    (714, 'Outrageous Orange', 0xFF6E4A),
    (715, 'Oxblood', 0x4A0000),
    (716, 'Oxford Blue', 0x002147),
    (717, 'Pacific Blue', 0x1CA9C9),
    (718, 'Palatinate Purple', 0x682860),
    (719, 'Pale', 0xDB7093),
    (720, 'Pale Aqua', 0xBCD4E6),
    (721, 'Pale Cerulean', 0x9BC4E2),
    (722, 'Pale Pink', 0xFADADD),
    (723, 'Pale Silver', 0xC9C0BB),
    (724, 'Pale Spring Bud', 0xECEBBD),
    (725, 'Pale Goldenrod', 0xEEE8AA),
    (726, 'Pale Green', 0x98FB98),
    (727, 'Pale Green1', 0x9AFF9A),
    (728, 'Light Green', 0x90EE90),
    (729, 'Pale Green3', 0x7CCD7C),
    (730, 'Pale Green4', 0x548B54),
    (731, 'Pale Turquoise', 0xAFEEEE),
    (732, 'Pale Turquoise1', 0xBBFFFF),
    (733, 'Pale Turquoise2', 0xAEEEEE),
    (734, 'Pale Turquoise3', 0x96CDCD),
    (735, 'Pale Turquoise4', 0x668B8B),
    (736, 'Pale Violet Red', 0xDB7093),
    (737, 'Pale Violet Red1', 0xFF82AB),
    (738, 'Pale Violet Red2', 0xEE799F),
    (739, 'Pale Violet Red3', 0xCD6889),
    (740, 'Pale Violet Red4', 0x8B475D),
    (741, 'Pansy Purple', 0x78184A),
    (742, 'Papaya Whip', 0xFFEFD5),
    (743, 'Paradise Pink', 0xE63E62),
    (744, 'Pastel Pink', 0xDEA5A4),
    (745, 'Patriarch (Purple)', 0x800080),
    (746, 'Peach', 0xFFE5B4),
    (747, 'Peach Puff1', 0xFFDAB9),
    (748, 'Peach Puff2', 0xEECBAD),
    (749, 'Peach Puff3', 0xCDAF95),
    (750, 'Peach Puff4', 0x8B7765),
    (751, 'Pear', 0xD1E231),
    (752, 'Pearly Purple', 0xB768A2),
    (753, 'Persian Blue', 0x1C39BB),
    (754, 'Persian Green', 0x00A693),
    (755, 'Persian Indigo', 0x32127A),
    (756, 'Persian Orange', 0xD99058),
    (757, 'Persian Pink', 0xF77FBE),
    (758, 'Persian Plum', 0x701C1C),
    (759, 'Persian Red', 0xCC3333),
    (760, 'Persian Rose', 0xFE28A2),
    (761, 'Pewter Blue', 0x8BA8B7),
    (762, 'Phthalo Blue', 0x000F89),
    (763, 'Phthalo Green', 0x123524),
    (764, 'Pictorial Carmine', 0xC30B4E),
    (765, 'Piggy Pink', 0xFDDDE6),
    (766, 'Pine Green', 0x01796F),
    (767, 'Pine Tree', 0x2A2F23),
    (768, 'Pink', 0xFFC0CB),
    (769, 'Pink (Pantone)', 0xD74894),
    (770, 'Pink Flamingo', 0xFC74FD),
    (771, 'Pink Sherbet', 0xF78FA7),
    (772, 'Pink1', 0xFFB5C5),
    (773, 'Pink2', 0xEEA9B8),
    (774, 'Pink3', 0xCD919E),
    (775, 'Pink4', 0x8B636C),
    (776, 'Pistachio', 0x93C572),
    (777, 'Platinum', 0xE5E4E2),
    (778, 'Plum', 0x8E4585),
    (779, 'Plum1', 0xFFBBFF),
    (780, 'Plum2', 0xEEAEEE),
    (781, 'Plum3', 0xCD96CD),
    (782, 'Plum4', 0x8B668B),
    (783, 'Plump Purple', 0x5946B2),
    (784, 'Portland Orange', 0xFF5A36),
    (785, 'Powder Blue', 0xB0E0E6),
    (786, 'Prussian Blue', 0x003153),
    (787, 'Puce', 0xCC8899),
    (788, 'Pumpkin', 0xFF7518),
    (789, 'Purple', 0xA020F0),
    (790, 'Purple1', 0x9B30FF),
    (791, 'Purple2', 0x912CEE),
    (792, 'Purple3', 0x7D26CD),
    (793, 'Purple4', 0x551A8B),
    (794, 'Quinacridone Magenta', 0x8E3A59),
    (795, 'Radical Red', 0xFF355E),
    (796, 'Raspberry', 0xE30B5D),
    (797, 'Razzmatazz', 0xE3256B),
    (798, 'Rebeccapurple', 0x663399),
    (799, 'Red Orange', 0xFF5349),
    (800, 'Bright Red', 0xFF0000),
    (801, 'Red2', 0xEE0000),
    (802, 'Red3', 0xCD0000),
    (803, 'Dark Red', 0x8B0000),
    (804, 'Redwood', 0xA45A52),
    (805, 'Rifle Green', 0x444C38),
    (806, 'Rocket Metallic', 0x8A7F80),
    (807, 'Rose', 0xFF007F),
    (808, 'Rose Bonbon', 0xF9429E),
    (809, 'Rose Dust', 0x9E5E6F),
    (810, 'Rose Pink', 0xFF66CC),
    (811, 'Rose Taupe', 0x905D5D),
    (812, 'Rosewood', 0x65000B),
    (813, 'Rosy Brown', 0xBC8F8F),
    (814, 'Rosy Brown1', 0xFFC1C1),
    (815, 'Rosy Brown2', 0xEEB4B4),
    (816, 'Rosy Brown3', 0xCD9B9B),
    (817, 'Rosy Brown4', 0x8B6969),
    (818, 'Royal Blue', 0x4169E1),
    (819, 'Royal Blue1', 0x4876FF),
    (820, 'Royal Blue2', 0x436EEE),
    (821, 'Royal Blue3', 0x3A5FCD),
    (822, 'Royal Blue4', 0x27408B),
    (823, 'Ruby', 0xE0115F),
    (824, 'Russet', 0x80461B),
    (825, 'Russian Green', 0x679267),
    (826, 'Russian Violet', 0x32174D),
    (827, 'Rust', 0xB7410E),
    (828, 'Saddle Brown', 0x8B4513),
    (829, 'Saffron', 0xF4C430),
    (830, 'Sage', 0xBCB88A),
    (831, 'Salmon', 0xFA8072),
    (832, 'Salmon1', 0xFF8C69),
    (833, 'Salmon2', 0xEE8262),
    (834, 'Salmon3', 0xCD7054),
    (835, 'Salmon4', 0x8B4C39),
    (836, 'Sandy Brown', 0xF4A460),
    (837, 'Sap Green', 0x507D2A),
    (838, 'Sapphire', 0x0F52BA),
    (839, 'Scarlet', 0xFF2400),
    (840, 'School Bus Yellow', 0xFFD800),
    (841, 'Sea Green1', 0x54FF9F),
    (842, 'Sea Green2', 0x4EEE94),
    (843, 'Sea Green3', 0x43CD80),
    (844, 'Sea Green4', 0x2E8B57),
    (845, 'Seal Brown', 0x59260B),
    (846, 'Seashell1', 0xFFF5EE),
    (847, 'Seashell2', 0xEEE5DE),
    (848, 'Seashell3', 0xCDC5BF),
    (849, 'Seashell4', 0x8B8682),
    (850, 'Selective Yellow', 0xFFBA00),
    (851, 'Sepia', 0x704214),
    (852, 'Shamrock Green', 0x009E60),
    (853, 'Shocking Pink', 0xFC0FC0),
    (854, 'Sienna', 0xA0522D),
    (855, 'Sienna1', 0xFF8247),
    (856, 'Sienna2', 0xEE7942),
    (857, 'Sienna3', 0xCD6839),
    (858, 'Sienna4', 0x8B4726),
    (859, 'Stainless Steel', 0xC0C0C0),
    (860, 'Silver Pink', 0xC4AEAD),
    (861, 'Sinopia', 0xCB410B),
    (862, 'Skobeloff', 0x007474),
    (863, 'Sky Blue', 0x87CEEB),
    (864, 'Sky Blue1', 0x87CEFF),
    (865, 'Sky Blue2', 0x7EC0EE),
    (866, 'Sky Blue3', 0x6CA6CD),
    (867, 'Sky Blue4', 0x4A708B),
    (868, 'Slate Blue', 0x6A5ACD),
    (869, 'Slate Blue1', 0x836FFF),
    (870, 'Slate Blue2', 0x7A67EE),
    (871, 'Slate Blue3', 0x6959CD),
    (872, 'Slate Blue4', 0x473C8B),
    (873, 'Slate Gray', 0x708090),
    (874, 'Slate Gray1', 0xC6E2FF),
    (875, 'Slate Gray2', 0xB9D3EE),
    (876, 'Slate Gray3', 0x9FB6CD),
    (877, 'Slate Gray4', 0x6C7B8B),
    (878, 'Smoky Black', 0x100C08),
    (879, 'Snow1', 0xFFFAFA),
    (880, 'Snow2', 0xEEE9E9),
    (881, 'Snow3', 0xCDC9C9),
    (882, 'Snow4', 0x8B8989),
    (883, 'Spanish Bistre', 0x807532),
    (884, 'Spanish Orange', 0xE86100),
    (885, 'Spanish Pink', 0xF7BFBE),
    (886, 'Spanish Viridian', 0x007F5C),
    (887, 'Spring Bud', 0xA7FC00),
    (888, 'Spring Frost', 0x87FF2A),
    (889, 'Spring Green1', 0x00FF7F),
    (890, 'Spring Green2', 0x00EE76),
    (891, 'Spring Green3', 0x00CD66),
    (892, 'Spring Green4', 0x008B45),
    (893, 'Steel Pink', 0xCC33CC),
    (894, 'Steel Blue', 0x4682B4),
    (895, 'Steel Blue1', 0x63B8FF),
    (896, 'Steel Blue2', 0x5CACEE),
    (897, 'Steel Blue3', 0x4F94CD),
    (898, 'Steel Blue4', 0x36648B),
    (899, 'Straw', 0xE4D96F),
    (900, 'Sunglow', 0xFFCC33),
    (901, 'Super Pink', 0xCF6BA9),
    (902, 'Sweet Brown', 0xA83731),
    (903, 'Tan', 0xD2B48C),
    (904, 'Tan1', 0xFFA54F),
    (905, 'Tan2', 0xEE9A49),
    (906, 'Tan3', 0xCD853F),
    (907, 'Tan4', 0x8B5A2B),
    (908, 'Tangerine', 0xF28500),
    (909, 'Tart Orange', 0xFB4D46),
    (910, 'Taupe', 0x483C32),
    (911, 'Taupe Gray', 0x8B8589),
    (912, 'Tea Green', 0xD0F0C0),
    (913, 'Teal', 0x008080),
    (914, 'Teal Blue', 0x367588),
    (915, 'Terra Cotta', 0xE2725B),
    (916, 'Thistle', 0xD8BFD8),
    (917, 'Thistle1', 0xFFE1FF),
    (918, 'Thistle2', 0xEED2EE),
    (919, 'Thistle3', 0xCDB5CD),
    (920, 'Thistle4', 0x8B7B8B),
    (921, 'Tiffany Blue', 0x0ABAB5),
    (922, 'Timberwolf', 0xDBD7D2),
    (923, 'Titanium Yellow', 0xEEE600),
    (924, 'Tomato1', 0xFF6347),
    (925, 'Tomato2', 0xEE5C42),
    (926, 'Tomato3', 0xCD4F39),
    (927, 'Tomato4', 0x8B3626),
    (928, 'Tropical Rainforest', 0x00755E),
    (929, 'Tumbleweed', 0xDEAA88),
    (930, 'Turquoise', 0x40E0D0),
    (931, 'Turquoise Blue', 0x00FFEF),
    (932, 'Turquoise1', 0x00F5FF),
    (933, 'Turquoise2', 0x00E5EE),
    (934, 'Turquoise3', 0x00C5CD),
    (935, 'Turquoise4', 0x00868B),
    (936, 'Tuscan Red', 0x7C4848),
    (937, 'Tuscany', 0xC09999),
    (938, 'Twilight Lavender', 0x8A496B),
    (939, 'Tyrian Purple', 0x66023C),
    (940, 'UP Forest Green', 0x014421),
    (941, 'UP Maroon', 0x7B1113),
    (942, 'Ultra Pink', 0xFF6FFF),
    (943, 'Ultramarine', 0x3F00FF),
    (944, 'Ultramarine Blue', 0x4166F5),
    (945, 'Unbleached Silk', 0xFFDDCA),
    (946, 'United Nations Blue', 0x5B92E5),
    (947, 'Upsdell Red', 0xAE2029),
    (948, 'Van Dyke Brown', 0x664228),
    (949, 'Vanilla', 0xF3E5AB),
    (950, 'Vanilla Ice', 0xF38FA9),
    (951, 'Vegas Gold', 0xC5B358),
    (952, 'Venetian Red', 0xC80815),
    (953, 'Verdigris', 0x43B3AE),
    (954, 'Vermillion', 0xE34234),
    (955, 'Violet Red', 0xD02090),
    (956, 'Violet Red1', 0xFF3E96),
    (957, 'Violet Red2', 0xEE3A8C),
    (958, 'Violet Red3', 0xCD3278),
    (959, 'Violet Red4', 0x8B2252),
    (960, 'Viridian', 0x40826D),
    (961, 'Viridian Green', 0x009698),
    (962, 'Vivid Burgundy', 0x9F1D35),
    (963, 'Vivid Sky Blue', 0x00CCFF),
    (964, 'Vivid Tangerine', 0xFFA089),
    (965, 'Vivid Violet', 0x9F00FF),
    (966, 'Volt', 0xCEFF00),
    (967, 'Warm Black', 0x004242),
    (968, 'Wheat', 0xF5DEB3),
    (969, 'Wheat1', 0xFFE7BA),
    (970, 'Wheat2', 0xEED8AE),
    (971, 'Wheat3', 0xCDBA96),
    (972, 'Wheat4', 0x8B7E66),
    (973, 'White Smoke', 0xF5F5F5),
    (974, 'Wild Blue Yonder', 0xA2ADD0),
    (975, 'Wild Orchid', 0xD470A2),
    (976, 'Wild Strawberry', 0xFF43A4),
    (977, 'Windsor Tan', 0xA75502),
    (978, 'Wine', 0x722F37),
    (979, 'Wintergreen Dream', 0x56887D),
    (980, 'Wisteria', 0xC9A0DC),
    (981, 'Xanadu', 0x738678),
    (982, 'Yellow Orange', 0xFFAE42),
    (983, 'Yellow Pantone', 0xFEDF00),
    (984, 'Yellow1', 0xFFFF00),
    (985, 'Yellow2', 0xEEEE00),
    (986, 'Yellow3', 0xCDCD00),
    (987, 'Yellow4', 0x8B8B00),
    (988, 'Yellow Green', 0x9ACD32),
    (989, 'Zaffre', 0x0014A8),
    (990, 'Zomp', 0x39A78E),
    (991, 'Blue Gray', 0x6699CC),
    (992, 'Nut Brown', 0x583827),
    (993, 'Leaf Green', 0x276235),
    (994, 'Claret Violet', 691639),
    (995, 'Signal Blue', 0x154889),
    (996, 'Water Blue', 0x007577),
    (997, 'Natural White', 0xF9F7F8),
    (998, 'Pastel Green', 0xC1E1C1),
    (999, 'Curry', 0x874010),
    (1000, 'Platinum Gray', 0xA8A9A3),
    (1001, 'Pure White', 0xFFFFFF),
    (1002, 'Heather Violet', 0xC4608C),
    (1003, 'Natural', 0xE5D3BF),
    (1004, 'Light Brown', 0xC4A484),
    (1005, 'Cream White', 0xFCFBF4),
    (1006, 'Light Purple', 0xCBC3E3),
    (1007, 'Curry Yellow', 0xE9DA89),
    (1008, 'Carmine Red', 0xFF0038),
    (1009, 'Pastel Orange', 0xFAC898),
    (1010, 'Grafe Violet', 0x4C2882),
    (1011, 'Gabriel', 0x4B3C8E),
    (1012, 'Brown Red', 0x7B3F00),
    (1013, 'Metal', 0xA9A9A9),
    (1014, 'Light Red', 0xFF4D4D),
    (1015, 'Cadillac Gray', 0xB2B1B0),
    (1016, 'Dark Purple', 0x301934),
    (1017, 'Silver', 0xC0C0C0),
    (1018, 'Multiple Colors', 0x000000),
    (1019, 'Transparent', 0xFFFFFF)
)


def get_color_id(color):
    color = color.title()
    if '-' in color:
        first, second = color.split('-', 1)
        color = second + ' ' + first

    color = color.replace('Grey', 'Gray')

    if color == 'Clear':
        color = 'Transparent'

    for id_, name, _ in color_data:
        if color == name:
            return id_

    raise RuntimeError(color)


field_mapping = {
    'itemsrsinterface_en': ('type_id', str),
    'itemsealtype_en': ('type_id', lambda x: x.title()),
    'itemconnectortype_en': ('type_id', str),
    'productseriesproductline_en': ('part_type_id', str),
    'itemdrmproductfamily_en': ('part_type_id', str),
    'itemresourcecrimpinformation_en': ('crimp_info_id', lambda x: x.split(', ')),
    'itemresourceimages_en': ('image_id', lambda x: x.split(', ')),
    'itemcablelength_en': ('length', float),
    'itemlength_en': ('length', float),
    'itemhsggender_en': ('gender_id', str),
    'itemtermgender_en': ('gender_id', str),
    'itemsrsinterfacecolor_en': ('color_id', get_color_id),
    'itemsealcolour_en': ('color_id', get_color_id),
    'itemcolour_en': ('color_id', get_color_id),
    'itemcablecolour_en': ('color_id', get_color_id),
    'itemmatingforce_en': ('mating_force_id', str),
    'producthsgconnectormatingforce_en': ('mating_force_id', str),
    'productmatingcycle_en': ('mating_cycles', int),
    'itemmatingcycle_en': ('mating_cycles', int),
    'productname_en': ('family_id', str),
    'itemparentname_en': ('series_id', str),
    'itemhsgcavities_en': ('num_cavities', int),
    'itemhvintercoways_en': ('num_cavities', int),
    'itemhvcurrent_en': ('current', str),
    'itemhvintercoamperage_en': ('current', str),
    'itemtermmaxcablecrosssection_en': ('wire_cross_max', float),
    'itemsrswirecrosssection_en': ('wire_cross_max', float),
    'itemhvintercocablerangemax_en': ('wire_dia_max', float),
    'itemsealcablediamax_en': ('wire_dia_max', float),
    'itemtermcablediametermax_en': ('wire_dia_max', float),
    'itemsrswireodmax_en': ('wire_dia_max', float),
    'itemhvintercocablerangemin_en': ('wire_dia_min', float),
    'itemsealcablediamin_en': ('wire_dia_min', float),
    'itemtermcablediametermin_en': ('wire_dia_min', float),
    'itemsrswireodmin_en': ('wire_dia_min', float),
    'itemcpa_en': ('has_cpa', lambda x: int(x == 'True')),
    'itemcabletype_en': ('cable_type_id', str),
    'iteminterfacetype_en': ('interface_type_id', str),
    'itemtermmincablecrosssection_en': ('wire_cross_min', float),
    'itemresource3ddrawings_en': ('model_3d_id', str),
    'productresourcedatasheets_en': ('datasheet_id', lambda x: x.split(', ')),
    'itemresourcedrawings_en': ('cad_id', lambda x: x.split(', ')),
    'competitorpartapn_en': ('competitor_part_number', str),
    'competitorpartcompetitorname_en': ('competitor_mfg_id', str),
    'itembladesizes_en': ('blade_sizes', str),
    'itemcablespec_en': ('wire_spec', str),
    'itemclipslot_en': ('clip_slot', int),
    'itemconfiguration_en': ('configuration_id', str),
    'itemconnectormatingstyle_en': ('mating_style_id', str),
    'itemdrmproductnamegroup_en': ('group_id', lambda x: x.title()),
    'itemfrequency_en': ('frequency_id', str),
    'itemgsddescription_en': ('description_id', str),
    'itemheight_en': ('height', float),
    'itemhsgbladesize1_en': ('blade_size_1', float),
    'itemhsgbladesize1qty_en': ('blade_size_1_qty', int),
    'itemhsgbladesize2_en': ('blade_size_2', float),
    'itemhsgbladesize2qty_en': ('blade_size_2_qty', int),
    'itemhsgbladesize3_en': ('blade_size_3', float),
    'itemhsgbladesize3qty_en': ('blade_size_3_qty', int),
    'itemhsgcavitiesusable_en': ('num_usable_cavities', int),
    'itemhsghybridtag_en': ('hybrid_tag_id', str),
    'itemhsgnetweight_en': ('weight', float),
    'itemhsgprimarylocktype_en': ('primary_lock_type_id', lambda x: x.title()),
    'itemhsgsealing_en': ('sealing', lambda x: int(x == 'True')),
    'itemhsgwiredirectioncableexitorientation_en': ('wire_direction_id', str),
    'itemhvintercoassemblyassurance_en': ('hv_intercon_aa_id', str),
    'itemhvintercocableshielding_en': ('shielding_id', str),
    'itemhvintercovoltage_en': ('voltage', str),
    'itemimpedance_en': ('impedance', str),
    'iteminsideringdiam_en': ('inside_ring_dia', float),
    'itemitemaccessories_en': ('compat_accessories', lambda x: [f"{itm.strip()}" for itm in x.split(',')]),
    'itemitemmatesto_en': ('mates_to', lambda x: [f"{itm.strip()}" for itm in x.split(',')]),
    'itemitemrelatedseals_en': ('compat_seals', lambda x: [f"{itm.strip()}" for itm in x.split(',')]),
    'itemitemrelatedterminals_en': ('compat_terminals', lambda x: [f"{itm.strip()}" for itm in x.split(',')]),
    'itemmaterial_en': ('material_id', str),
    'itemnophaseaccurrent_en': ('num_phases', int),
    'itempartnumberapn_en': ('part_number', str),
    'itempimitemdescription_en': ('description', str),
    'itemrestraintring_en': ('restraint_ring', lambda x: x == 'True'),
    'itemsealbareholediameter_en': ('seal_bore_dia', float),
    'itemsealcavitysize_en': ('cavity_size', float),
    'itemsealhardness_en': ('hardness', int),
    'itemsealoilcontent_en': ('oil_content_id', str),
    'itemsealoutsidediameter_en': ('outside_dia', float),
    'itemsealsubtype_en': ('sub_type_id', lambda x: x.title()),
    'itemsrsproductname_en': ('product_name_id', str),
    'itemtermbladesize_en': ('blade_size', float),
    'itemtermlockingmechanism_en': ('lock_type_id', lambda x: x.title()),
    'itemtermplating_en': ('plating_id', str),
    'itemtermsealing_en': ('sealing_id', str),
    'itemwidth_en': ('width', float),
    'productapplication1_en': ('prod_app1_id', str),
    'productapplication2_en': ('prod_app2_id', str),
    'productapplication3_en': ('prod_app3_id', str),
    'productbenefit1_en': ('benefit1_id', str),
    'productbenefit2_en': ('benefit2_id', str),
    'productbenefit3_en': ('benefit3_id', str),
    'productbenefit4_en': ('benefit4_id', str),
    'productbenefit5_en': ('benefit5_id', str),
    'productbenefit6_en': ('benefit6_id', str),
    'productconnectionlevel_en': ('connection_type_id', str),
    'productfeature1_en': ('feature1_id', str),
    'productfeature2_en': ('feature2_id', str),
    'productfeature3_en': ('feature3_id', str),
    'productfeature4_en': ('feature4_id', str),
    'productfeature5_en': ('feature5_id', str),
    'productfeature6_en': ('feature6_id', str),
    'productmarketingname_en': ('marketing_name_id', str),
    'productmarketingnameext_en': ('marketing_name_ext_id', str),
    'productproductmarket_en': ('prod_market_id', str),
    'productproductoverview_en': ('overview_id', str),
    'productsealingrating_en': ('ip_rating_id', str),
    'producttempmax_en': ('max_temp_id', str),
    'producttempmin_en': ('min_temp_id', str),
    'productvibration_en': ('vibration_rating', str),
    'productoncarapplication_en': ('application_id', str),
}

output_connectors = []

for result in connectors:
    all_fields = all_fields.union(set(list(result.keys())))

    con_data = {}
    for field, value in result.items():

        if field not in connectors_fields:
            connectors_fields[field] = set()

        connectors_fields[field] = connectors_fields[field].union(value)

        if field in (
            'itemvalidin_en', 'language', 'lastupdated', 'url_en', 'productresourceimages_en', 'productid', 'channelnodeproducts_en',
            'childpartnumbers_en', 'competitorpartapn_en_test', 'competitorpartbuiltdescription_en', 'itemapplicationconstraintsdescription_en',
            'itemcoding_en', 'itemcomponenttype_en', 'itemconnectorpositionassurance_en', 'itemdimestatus_en', 'itemdrmproductline_en',
            'itemelvcompliant_en', 'itemgsdfamily_en', 'itemgsdseries_en', 'itemhsgpartofmodule_en', 'itemhsgsealquantity_en',
            'itemitemmatestotypes_en', 'itemlegacypartnumbercrossref_en', 'itemmanufacturingsite_en', 'itemminorderquantityunits_en',
            'itemmousermanufacturerpn_en', 'itemrelation_en', 'itempimstatus_en', 'itemrestrictedusagedesigncontrol_en',
            'itemrohscompliant_en', 'itemsampleprogramavailable_en', 'itemsealbareholediameter_en', 'itemsealcablediamax_en',
            'itemsealcablediamin_en', 'itemsealcavitysize_en', 'itemsealhardness_en', 'itemsealoutsidediameter_en', 'itemsrsemiprotection_en',
            'itemsrstermination_en', 'itemsrswatertight_en', 'itemsrswiresize_en', 'itemstandardpackagequantity_en', 'itemtermcablediametermax_en',
            'itemtermcablediametermin_en', 'itemterminalpositionassurance_en', 'itemtermmaxcablecrosssection_en', 'itemtermmincablecrosssection_en',
            'itemtermreelsize_en', 'itemtermsingleterminal_en', 'itemvalidin_en', 'productbrochurefilename_en', 'productcataloguefilename_en',
            'productconnectortype_en', 'productdatasheetfilename_en', 'productpimstatus_en', 'productproduct_en', 'productresourcecatalogue_en',
            'productresourcebrochure_en', 'productresourcepresentation_en', 'productsealingclass_en', 'productvalidin_en',
            'url_en', 'itemsrsserviceable_en', 'itemreachcompliant_en', 'itemparentid_en', 'itemnoofpin_en', 'itemhvintercohvil_en',
            'itempartstatus_en', 'competitorpartcompetitorname_en'
        ):
            continue

        if field == 'itemitemaccessories_en':
            value[0] = value[0].replace(', RESOURCE-CENTER-ITEM', '')

        field, type = field_mapping[field]
        con_data[field] = type(value[:][0])

    output_connectors.append(con_data)


with open(r'connectors.json', 'w') as f:
    f.write(json.dumps(output_connectors, indent=4))


print('CONNECTORS')

for key in sorted(list(connectors_fields.keys())):
    print(key)
    for value in sorted(list(connectors_fields[key])):
        print('   ', value)

print()


output_seals = []

for result in seals:
    all_fields = all_fields.union(set(list(result.keys())))

    seal_data = {}

    for field, value in result.items():
        if field not in seals_fields:
            seals_fields[field] = set()

        seals_fields[field] = seals_fields[field].union(value)

        if field in (
            'childpartnumbers_en', 'competitorpartapn_en_test', 'competitorpartcompetitorname_en',
            'itemapplicationconstraintsdescription_en', 'itemclipslot_en', 'itemconnectorpositionassurance_en',
            'itemcpa_en', 'itemdimestatus_en', 'itemdrmproductfamily_en', 'itemdrmproductline_en',
            'itemelvcompliant_en', 'itemgsdfamily_en', 'itemhsgbladesize1qty_en', 'itemhsgbladesize2qty_en', 'itemhsgbladesize3qty_en',
            'itemhsgcavities_en', 'itemhsgcavitiesusable_en', 'itemhsgpartofmodule_en', 'itemhsgsealing_en', 'itemhsgsealquantity_en',
            'itemhvintercocablerangemax_en', 'itemhvintercocablerangemin_en', 'itemhvintercohvil_en',
            'itemhvintercoways_en', 'itemitemrelatedseals_en', 'itemlegacypartnumbercrossref_en', 'itemmanufacturingsite_en',
            'itemminorderquantityunits_en', 'itemmousermanufacturerpn_en', 'itemnoofpin_en', 'itemparentid_en',
            'itempartstatus_en', 'itempimstatus_en', 'itemreachcompliant_en', 'itemrelation_en',
            'itemrestrictedusagedesigncontrol_en', 'itemrohscompliant_en', 'itemsampleprogramavailable_en',
            'itemsealsealshape_en', 'itemsrsserviceable_en', 'itemsrswatertight_en', 'itemsrswirecrosssection_en',
            'itemsrswireodmax_en', 'itemsrswireodmin_en', 'itemsrswiresize_en', 'itemstandardpackagequantity_en',
            'itemtermcablediametermax_en', 'itemtermcablediametermin_en', 'itemterminalpositionassurance_en',
            'itemtermmaxcablecrosssection_en', 'itemtermmincablecrosssection_en', 'itemtermreelsize_en',
            'itemtermsingleterminal_en', 'itemvalidin_en', 'itemwidth_en', 'language', 'lastupdated',
            'productcataloguefilename_en', 'productid', 'productpimstatus_en', 'productresourcecatalogue_en',
            'productseriesproductline_en', 'productvalidin_en', 'url_en', 'itemcomponenttype_en', 'productresourceimages_en',
            'competitorpartbuiltdescription_en', 'channelnodeproducts_en', 'itemgsddescription_en',
            'productproductoverview_en'

        ):
            continue

        field, type = field_mapping[field]
        seal_data[field] = type(value[:][0])

    output_seals.append(seal_data)

with open(r'seals.json', 'w') as f:
    f.write(json.dumps(output_seals, indent=4))


print('SEALS')

for key in sorted(list(seals_fields.keys())):
    print(key)
    for value in sorted(list(seals_fields[key])):
        print('   ', value)

print()


output_terminals = []

for result in terminals:
    all_fields = all_fields.union(set(list(result.keys())))
    terminal_data = {}

    for field, value in result.items():
        if field not in terminals_fields:
            terminals_fields[field] = set()

        terminals_fields[field] = terminals_fields[field].union(value)

        if field in (
            'channelnodeproducts_en', 'childpartnumbers_en', 'competitorpartapn_en_test',
            'competitorpartbuiltdescription_en', 'competitorpartcompetitorname_en',
            'itemapplicationconstraintsdescription_en', 'itemclipslot_en', 'itemcomponenttype_en',
            'itemconnectorpositionassurance_en', 'itemcpa_en', 'itemdimestatus_en',
            'itemdrmproductfamily_en', 'itemdrmproductline_en', 'itemelvcompliant_en',
            'itemgsdfamily_en', 'itemheight_en', 'itemhsgbladesize1qty_en', 'itemhsgbladesize2qty_en',
            'itemhsgbladesize3qty_en', 'itemhsgcavities_en', 'itemhsgcavitiesusable_en',
            'itemhsgpartofmodule_en', 'itemhsgsealing_en', 'itemhsgsealquantity_en',
            'itemhvintercocablerangemax_en', 'itemhvintercocablerangemin_en', 'itemhvintercohvil_en',
            'itemhvintercoways_en', 'itemlegacypartnumbercrossref_en', 'itemmanufacturingsite_en',
            'itemminorderquantityunits_en', 'itemmousermanufacturerpn_en', 'itemnoofpin_en',
            'itemparentid_en', 'itemparentname_en', 'itempartstatus_en', 'itempimstatus_en',
            'itemreachcompliant_en', 'itemrelation_en', 'itemrestrictedusagedesigncontrol_en',
            'itemrohscompliant_en', 'itemsampleprogramavailable_en', 'itemsealbareholediameter_en',
            'itemsealcablediamax_en', 'itemsealcablediamin_en', 'itemsealcavitysize_en',
            'itemsealhardness_en', 'itemsealoutsidediameter_en', 'itemsrsserviceable_en',
            'itemsrswatertight_en', 'itemsrswirecrosssection_en', 'itemsrswireodmax_en',
            'itemsrswireodmin_en', 'itemsrswiresize_en', 'itemstandardpackagequantity_en',
            'itemterminalpositionassurance_en', 'itemtermreelsize_en', 'itemtermsingleterminal_en',
            'itemvalidin_en', 'itemwidth_en', 'language', 'lastupdated', 'productbrochurefilename_en',
            'productcataloguefilename_en', 'productdatasheetfilename_en', 'productid',
            'productpimstatus_en', 'productproduct_en', 'productproductmarket_en', 'productproductoverview_en',
            'productresourcebrochure_en', 'productresourcecatalogue_en', 'productseriesproductline_en',
            'productvalidin_en', 'url_en', 'productresourceimages_en'

        ):
            continue

        field, type = field_mapping[field]
        terminal_data[field] = type(value[:][0])

    output_terminals.append(terminal_data)


with open(r'terminals.json', 'w') as f:
    f.write(json.dumps(output_terminals, indent=4))

print('TERMINALS')

for key in sorted(list(terminals_fields.keys())):
    print(key)
    for value in sorted(list(terminals_fields[key])):
        print('   ', value)

print()


output_accessories = []

for result in accessories:
    all_fields = all_fields.union(set(list(result.keys())))

    accessory_data = {}

    for field, value in result.items():
        if field not in accessories_fields:
            accessories_fields[field] = set()

        accessories_fields[field] = accessories_fields[field].union(value)

        accessory_type = accessory_data.get('accessory_type_id', 'Unknown')

        if field == 'itemgsdfamily_en' and accessory_type == 'Unknown':
            accessory_type = value[0]
            mapping = {
                'CBL/CONN': 'CPA',
                'CONN LK': 'CPA',
                'COV': 'Cover',
                'CPA': 'CPA',
                'INSERT': 'Unknown',
                'PLR': 'PLR',
                'RETAINER': 'Unknown',
                'SECONDARY': 'TPA',
                'STRAIN RLF': 'Strain',
                'TERM LK': 'TPA',
                'TPA/CLIP': 'TPA',
                'TPA/SEAL': 'TPA'
            }
            accessory_data['accessory_type_id'] = mapping[accessory_type]

        if field == 'itemparentid_en' and accessory_type == 'Unknown':
            if value[0] == 'ACC-COVER':
                accessory_data['accessory_type_id'] = 'Cover'

        if field in ('itemgsddescription_en', 'itempimitemdescription_en') and accessory_type == 'Unknown':
            accessory_type = value[0]
            if 'CPA' in accessory_type:
                accessory_type = 'CPA'
            elif 'LEVER' in accessory_type:
                accessory_type = 'CPA'
            elif 'LOCK COV' in accessory_type:
                accessory_type = 'CPA'
            elif 'RETAINER SEAL' in accessory_type:
                accessory_type = 'Seal Retainer'
            elif 'RETAINER' in accessory_type:
                accessory_type = 'CPA'
            elif 'SLIDE' in accessory_type:
                accessory_type = 'CPA'
            elif 'TPA' in accessory_type:
                accessory_type = 'TPA'
            elif 'COMB' in accessory_type:
                accessory_type = 'TPA'
            elif 'PLATE' in accessory_type:
                accessory_type = 'TPA'
            elif 'SLC' in accessory_type:
                accessory_type = 'TPA'
            elif 'SECONDARY' in accessory_type:
                accessory_type = 'TPA'
            elif 'PLR' in accessory_type:
                accessory_type = 'PLR'
            elif 'STRAIN' in accessory_type:
                accessory_type = 'Strain'
            else:
                accessory_type = 'Unknown'

            accessory_data['accessory_type_id'] = accessory_type

        if field in (
            'competitorpartapn_en_test', 'competitorpartbuiltdescription_en', 'competitorpartcompetitorname_en',
            'itemapplicationconstraintsdescription_en', 'itemclipslot_en', 'itemconnectorpositionassurance_en',
            'itemcomponenttype_en', 'itemcpa_en', 'itemdrmproductfamily_en', 'itemdrmproductline_en',
            'itemelvcompliant_en', 'itemheight_en', 'itemhsgbladesize1qty_en', 'itemhsgbladesize2qty_en',
            'itemhsgbladesize3qty_en', 'itemhsgcavities_en', 'itemhsgcavitiesusable_en', 'itemhsgpartofmodule_en',
            'itemhsgsealing_en', 'itemhsgsealquantity_en', 'itemhvintercocablerangemax_en',
            'itemhvintercocablerangemin_en', 'itemhvintercohvil_en', 'itemhvintercoways_en',
            'itemlegacypartnumbercrossref_en', 'itemmanufacturingsite_en', 'itemminorderquantityunits_en',
            'itemmousermanufacturerpn_en', 'itemnoofpin_en', 'itemparentid_en', 'itemparentname_en',
            'itempimstatus_en', 'itemreachcompliant_en', 'itemrelation_en', 'itemrestrictedusagedesigncontrol_en',
            'itemrohscompliant_en', 'itemsampleprogramavailable_en', 'itemsealbareholediameter_en',
            'itemsealcablediamax_en', 'itemsealcablediamin_en', 'itemsealcavitysize_en',
            'itemsealhardness_en', 'itemsealoutsidediameter_en', 'itemsrsserviceable_en',
            'itemsrswatertight_en', 'itemsrswirecrosssection_en', 'itemsrswireodmax_en',
            'itemsrswireodmin_en', 'itemsrswiresize_en', 'itemstandardpackagequantity_en',
            'itemtermcablediametermax_en', 'itemtermcablediametermin_en',  'itemterminalpositionassurance_en',
            'itemtermmaxcablecrosssection_en', 'itemtermmincablecrosssection_en', 'itemtermreelsize_en',
            'itemtermsingleterminal_en', 'itemvalidin_en', 'itemwidth_en', 'language',
            'lastupdated', 'productid', 'productmarketingname_en', 'productseriesproductline_en',
            'url_en', 'itemparentid_en', 'itemgsdfamily_en', 'productresourceimages_en', 'itemgsddescription_en'
        ):
            continue

        field, type = field_mapping[field]
        accessory_data[field] = type(value[:][0])

    output_accessories.append(accessory_data)


print('ACCESSORIES')

with open(r'accessories.json', 'w') as f:
    f.write(json.dumps(output_accessories, indent=4))


for key in sorted(list(accessories_fields.keys())):
    print(key)
    for value in sorted(list(accessories_fields[key])):
        print('   ', value)

print()

print('HVI')
print(len(hv_interconnects))
print()
#
# for result in hv_interconnects:
#     all_fields = all_fields.union(set(list(result.keys())))
#     # check_types(result)
#
#     for field, value in result.items():
#         if field not in hv_interconnects_fields:
#             hv_interconnects_fields[field] = set()
#
#         hv_interconnects_fields[field] = hv_interconnects_fields[field].union(value)
#

# for key in sorted(list(hv_interconnects_fields.keys())):
#     print(key)
#     for value in sorted(list(hv_interconnects_fields[key])):
#         print('   ', value)

# print()
#
# for result in pin_headers:
#     all_fields = all_fields.union(set(list(result.keys())))
#
#     for field, value in result.items():
#         if field not in pin_headers_fields:
#             pin_headers_fields[field] = set()
#
#         pin_headers_fields[field] = pin_headers_fields[field].union(value)


print('PIN HEADERS')
print(len(pin_headers))

#
# for key in sorted(list(pin_headers_fields.keys())):
#     print(key)
#     for value in sorted(list(pin_headers_fields[key])):
#         print('   ', value)
#
# print()

#
# for result in high_voltage_charging:
#     all_fields = all_fields.union(set(list(result.keys())))
#
#     for field, value in result.items():
#         if field not in high_voltage_charging_fields:
#             high_voltage_charging_fields[field] = set()
#
#         high_voltage_charging_fields[field] = high_voltage_charging_fields[field].union(value)
#

print('HVC')
print(len(high_voltage_charging))
#
# for key in sorted(list(high_voltage_charging_fields.keys())):
#     print(key)
#     for value in sorted(list(high_voltage_charging_fields[key])):
#         print('   ', value)
#
# print()

#
# for result in srs:
#     all_fields = all_fields.union(set(list(result.keys())))
#
#     for field, value in result.items():
#         if field not in srs_fields:
#             srs_fields[field] = set()
#
#         srs_fields[field] = srs_fields[field].union(value)


print('SRS')
print(len(srs))

#
# for key in sorted(list(srs_fields.keys())):
#     print(key)
#     for value in sorted(list(srs_fields[key])):
#         print('   ', value)
#
# print()
#
# for result in high_speed:
#     all_fields = all_fields.union(set(list(result.keys())))
#
#     for field, value in result.items():
#         if field not in high_speed_fields:
#             high_speed_fields[field] = set()
#
#         high_speed_fields[field] = high_speed_fields[field].union(value)


print('HIGH SPEED')
print(len(high_speed))

#
# for key in sorted(list(high_speed_fields.keys())):
#     print(key)
#     for value in sorted(list(high_speed_fields[key])):
#         print('   ', value)
#
#
print()
output_covers = []

for result in covers:
    all_fields = all_fields.union(set(list(result.keys())))

    cover_data = {}

    for field, value in result.items():
        if field not in covers_fields:
            covers_fields[field] = set()

        covers_fields[field] = covers_fields[field].union(value)

        if field in (
            'competitorpartapn_en_test', 'competitorpartbuiltdescription_en', 'competitorpartcompetitorname_en',
            'itemapplicationconstraintsdescription_en', 'itemclipslot_en', 'itemcomponenttype_en',
            'itemconnectorpositionassurance_en', 'itemcpa_en', 'itemdrmproductfamily_en',
            'itemdrmproductline_en', 'itemelvcompliant_en', 'itemhsgbladesize1qty_en',
            'itemhsgbladesize2qty_en', 'itemhsgbladesize3qty_en', 'itemhsgcavities_en',
            'itemhsgcavitiesusable_en', 'itemhsghybridtag_en', 'itemhsgpartofmodule_en',
            'itemhsgsealing_en', 'itemhsgsealquantity_en', 'itemhvintercocablerangemax_en',
            'itemhvintercocablerangemin_en', 'itemhvintercohvil_en', 'itemhvintercoways_en',
            'itemitemmatestotypes_en', 'itemlegacypartnumbercrossref_en', 'itemmanufacturingsite_en',
            'itemminorderquantityunits_en', 'itemmousermanufacturerpn_en', 'itemnoofpin_en',
            'itemparentid_en', 'itemparentname_en', 'itempimstatus_en', 'itemreachcompliant_en',
            'itemrelation_en', 'itemrestrictedusagedesigncontrol_en', 'itemrohscompliant_en',
            'itemsampleprogramavailable_en', 'itemsealbareholediameter_en', 'itemsealcablediamax_en',
            'itemsealcablediamin_en', 'itemsealcavitysize_en', 'itemsealhardness_en',
            'itemsealoutsidediameter_en', 'itemsrsserviceable_en', 'itemsrswatertight_en',
            'itemsrswirecrosssection_en', 'itemsrswireodmax_en', 'itemsrswireodmin_en',
            'itemsrswiresize_en', 'itemstandardpackagequantity_en', 'itemtermcablediametermax_en',
            'itemtermcablediametermin_en', 'itemterminalpositionassurance_en',
            'itemtermmaxcablecrosssection_en', 'itemtermmincablecrosssection_en',
            'itemtermreelsize_en', 'itemtermsingleterminal_en', 'itemvalidin_en',
            'language', 'lastupdated', 'productid', 'productseriesproductline_en',
            'url_en', 'productresourceimages_en', 'itemgsdfamily_en', 'itemgsddescription_en'
        ):
            continue

        field, type = field_mapping[field]
        cover_data[field] = type(value[:][0])

    output_covers.append(cover_data)


with open(r'covers.json', 'w') as f:
    f.write(json.dumps(output_covers, indent=4))


print('COVERS')
print(len(covers))

for key in sorted(list(covers_fields.keys())):
    print(key)
    for value in sorted(list(covers_fields[key])):
        print('   ', value)

print()

for result in boots:
    all_fields = all_fields.union(set(list(result.keys())))

    for field, value in result.items():
        if field not in boots_fields:
            boots_fields[field] = set()

        boots_fields[field] = boots_fields[field].union(value)


print('BOOTS')
print(len(boots))

#
# for key in sorted(list(boots_fields.keys())):
#     print(key)
#     for value in sorted(list(boots_fields[key])):
#         print('   ', value)
#
#
# print()
#
# for item in sorted(list(all_fields)):
#     print(item)
