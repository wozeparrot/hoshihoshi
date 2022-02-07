import cv2
import numpy as np

from hh.utils import eprint


MODEL_POINTS = np.array([[0.000000, -3.406404, 5.979507],
                [0.000000, -1.126865, 7.475604],
                [0.000000, -2.089024, 6.058267],
                [-0.463928, 0.955357, 6.633583],
                [0.000000, -0.463170, 7.586580],
                [0.000000, 0.365669, 7.242870],
                [0.000000, 2.473255, 5.788627],
                [-4.253081, 2.577646, 3.279702],
                [0.000000, 4.019042, 5.284764],
                [0.000000, 4.885979, 5.385258],
                [0.000000, 8.261778, 4.481535],
                [0.000000, -3.706811, 5.864924],
                [0.000000, -3.918301, 5.569430],
                [0.000000, -3.994436, 5.219482],
                [0.000000, -4.542400, 5.404754],
                [0.000000, -4.745577, 5.529457],
                [0.000000, -5.019567, 5.601448],
                [0.000000, -5.365123, 5.535441],
                [0.000000, -6.149624, 5.071372],
                [0.000000, -1.501095, 7.112196],
                [-0.416106, -1.466449, 6.447657],
                [-7.087960, 5.434801, 0.099620],
                [-2.628639, 2.035898, 3.848121],
                [-3.198363, 1.985815, 3.796952],
                [-3.775151, 2.039402, 3.646194],
                [-4.465819, 2.422950, 3.155168],
                [-2.164289, 2.189867, 3.851822],
                [-3.208229, 3.223926, 4.115822],
                [-2.673803, 3.205337, 4.092203],
                [-3.745193, 3.165286, 3.972409],
                [-4.161018, 3.059069, 3.719554],
                [-5.062006, 1.934418, 2.776093],
                [-2.266659, -7.425768, 4.389812],
                [-4.445859, 2.663991, 3.173422],
                [-7.214530, 2.263009, 0.073150],
                [-5.799793, 2.349546, 2.204059],
                [-2.844939, -0.720868, 4.433130],
                [-0.711452, -3.329355, 5.877044],
                [-0.606033, -3.924562, 5.444923],
                [-1.431615, -3.500953, 5.496189],
                [-1.914910, -3.803146, 5.028930],
                [-1.131043, -3.973937, 5.189648],
                [-1.563548, -4.082763, 4.842263],
                [-2.650112, -5.003649, 4.188483],
                [-0.427049, -1.094134, 7.360529],
                [-0.496396, -0.475659, 7.440358],
                [-5.253307, 3.881582, 3.363159],
                [-1.718698, 0.974609, 4.558359],
                [-1.608635, -0.942516, 5.814193],
                [-1.651267, -0.610868, 5.581319],
                [-4.765501, -0.701554, 3.534632],
                [-0.478306, 0.295766, 7.101013],
                [-3.734964, 4.508230, 4.550454],
                [-4.588603, 4.302037, 4.048484],
                [-6.279331, 6.615427, 1.425850],
                [-1.220941, 4.142165, 5.106035],
                [-2.193489, 3.100317, 4.000575],
                [-3.102642, -4.352984, 4.095905],
                [-6.719682, -4.788645, -1.745401],
                [-1.193824, -1.306795, 5.737747],
                [-0.729766, -1.593712, 5.833208],
                [-2.456206, -4.342621, 4.283884],
                [-2.204823, -4.304508, 4.162499],
                [-4.985894, 4.802461, 3.751977],
                [-1.592294, -1.257709, 5.456949],
                [-2.644548, 4.524654, 4.921559],
                [-2.760292, 5.100971, 5.015990],
                [-3.523964, 8.005976, 3.729163],
                [-5.599763, 5.715470, 2.724259],
                [-3.063932, 6.566144, 4.529981],
                [-5.720968, 4.254584, 2.830852],
                [-6.374393, 4.785590, 1.591691],
                [-0.672728, -3.688016, 5.737804],
                [-1.262560, -3.787691, 5.417779],
                [-1.732553, -3.952767, 5.000579],
                [-1.043625, -1.464973, 5.662455],
                [-2.321234, -4.329069, 4.258156],
                [-2.056846, -4.477671, 4.520883],
                [-2.153084, -4.276322, 4.038093],
                [-0.946874, -1.035249, 6.512274],
                [-1.469132, -4.036351, 4.604908],
                [-1.024340, -3.989851, 4.926693],
                [-0.533422, -3.993222, 5.138202],
                [-0.769720, -6.095394, 4.985883],
                [-0.699606, -5.291850, 5.448304],
                [-0.669687, -4.949770, 5.509612],
                [-0.630947, -4.695101, 5.449371],
                [-0.583218, -4.517982, 5.339869],
                [-1.537170, -4.423206, 4.745470],
                [-1.615600, -4.475942, 4.813632],
                [-1.729053, -4.618680, 4.854463],
                [-1.838624, -4.828746, 4.823737],
                [-2.368250, -3.106237, 4.868096],
                [-7.542244, -1.049282, -2.431321],
                [0.000000, -1.724003, 6.601390],
                [-1.826614, -4.399531, 4.399021],
                [-1.929558, -4.411831, 4.497052],
                [-0.597442, -2.013686, 5.866456],
                [-1.405627, -1.714196, 5.241087],
                [-0.662449, -1.819321, 5.863759],
                [-2.342340, 0.572222, 4.294303],
                [-3.327324, 0.104863, 4.113860],
                [-1.726175, -0.919165, 5.273355],
                [-5.133204, 7.485602, 2.660442],
                [-4.538641, 6.319907, 3.683424],
                [-3.986562, 5.109487, 4.466315],
                [-2.169681, -5.440433, 4.455874],
                [-1.395634, 5.011963, 5.316032],
                [-1.619500, 6.599217, 4.921106],
                [-1.891399, 8.236377, 4.274997],
                [-4.195832, 2.235205, 3.375099],
                [-5.733342, 1.411738, 2.431726],
                [-1.859887, 2.355757, 3.843181],
                [-4.988612, 3.074654, 3.083858],
                [-1.303263, 1.416453, 4.831091],
                [-1.305757, -0.672779, 6.415959],
                [-6.465170, 0.937119, 1.689873],
                [-5.258659, 0.945811, 2.974312],
                [-4.432338, 0.722096, 3.522615],
                [-3.300681, 0.861641, 3.872784],
                [-2.430178, 1.131492, 4.039035],
                [-1.820731, 1.467954, 4.224124],
                [-0.563221, 2.307693, 5.566789],
                [-6.338145, -0.529279, 1.881175],
                [-5.587698, 3.208071, 2.687839],
                [-0.242624, -1.462857, 7.071491],
                [-1.611251, 0.339326, 4.895421],
                [-7.743095, 2.364999, -2.005167],
                [-1.391142, 1.851048, 4.448999],
                [-1.785794, -0.978284, 4.850470],
                [-4.670959, 2.664461, 3.084075],
                [-1.333970, -0.283761, 6.097047],
                [-7.270895, -2.890917, -2.252455],
                [-1.856432, 2.585245, 3.757904],
                [-0.923388, 0.073076, 6.671944],
                [-5.000589, -6.135128, 1.892523],
                [-5.085276, -7.178590, 0.714711],
                [-7.159291, -0.811820, -0.072044],
                [-5.843051, -5.248023, 0.924091],
                [-6.847258, 3.662916, 0.724695],
                [-2.412942, -8.258853, 4.119213],
                [-0.179909, -1.689864, 6.573301],
                [-2.103655, -0.163946, 4.566119],
                [-6.407571, 2.236021, 1.560843],
                [-3.670075, 2.360153, 3.635230],
                [-3.177186, 2.294265, 3.775704],
                [-2.196121, -4.598322, 4.479786],
                [-6.234883, -1.944430, 1.663542],
                [-1.292924, -9.295920, 4.094063],
                [-3.210651, -8.533278, 2.802001],
                [-4.068926, -7.993109, 1.925119],
                [0.000000, 6.545390, 5.027311],
                [0.000000, -9.403378, 4.264492],
                [-2.724032, 2.315802, 3.777151],
                [-2.288460, 2.398891, 3.697603],
                [-1.998311, 2.496547, 3.689148],
                [-6.130040, 3.399261, 2.038516],
                [-2.288460, 2.886504, 3.775031],
                [-2.724032, 2.961810, 3.871767],
                [-3.177186, 2.964136, 3.876973],
                [-3.670075, 2.927714, 3.724325],
                [-4.018389, 2.857357, 3.482983],
                [-7.555811, 4.106811, -0.991917],
                [-4.018389, 2.483695, 3.440898],
                [0.000000, -2.521945, 5.932265],
                [-1.776217, -2.683946, 5.213116],
                [-1.222237, -1.182444, 5.952465],
                [-0.731493, -2.536683, 5.815343],
                [0.000000, 3.271027, 5.236015],
                [-4.135272, -6.996638, 2.671970],
                [-3.311811, -7.660815, 3.382963],
                [-1.313701, -8.639995, 4.702456],
                [-5.940524, -6.223629, -0.631468],
                [-1.998311, 2.743838, 3.744030],
                [-0.901447, 1.236992, 5.754256],
                [0.000000, -8.765243, 4.891441],
                [-2.308977, -8.974196, 3.609070],
                [-6.954154, -2.439843, -0.131163],
                [-1.098819, -4.458788, 5.120727],
                [-1.181124, -4.579996, 5.189564],
                [-1.255818, -4.787901, 5.237051],
                [-1.325085, -5.106507, 5.205010],
                [-1.546388, -5.819392, 4.757893],
                [-1.953754, -4.183892, 4.431713],
                [-2.117802, -4.137093, 4.555096],
                [-2.285339, -4.051196, 4.582438],
                [-2.850160, -3.665720, 4.484994],
                [-5.278538, -2.238942, 2.861224],
                [-0.946709, 1.907628, 5.196779],
                [-1.314173, 3.104912, 4.231404],
                [-1.780000, 2.860000, 3.881555],
                [-1.845110, -4.098880, 4.247264],
                [-5.436187, -4.030482, 2.109852],
                [-0.766444, 3.182131, 4.861453],
                [-1.938616, -6.614410, 4.521085],
                [0.000000, 1.059413, 6.774605],
                [-0.516573, 1.583572, 6.148363],
                [0.000000, 1.728369, 6.316750],
                [-1.246815, 0.230297, 5.681036],
                [0.000000, -7.942194, 5.181173],
                [0.000000, -6.991499, 5.153478],
                [-0.997827, -6.930921, 4.979576],
                [-3.288807, -5.382514, 3.795752],
                [-2.311631, -1.566237, 4.590085],
                [-2.680250, -6.111567, 4.096152],
                [-3.832928, -1.537326, 4.137731],
                [-2.961860, -2.274215, 4.440943],
                [-4.386901, -2.683286, 3.643886],
                [-1.217295, -7.834465, 4.969286],
                [-1.542374, -0.136843, 5.201008],
                [-3.878377, -6.041764, 3.311079],
                [-3.084037, -6.809842, 3.814195],
                [-3.747321, -4.503545, 3.726453],
                [-6.094129, -3.205991, 1.473482],
                [-4.588995, -4.728726, 2.983221],
                [-6.583231, -3.941269, 0.070268],
                [-3.492580, -3.195820, 4.130198],
                [-1.255543, 0.802341, 5.307551],
                [-1.126122, -0.933602, 6.538785],
                [-1.443109, -1.142774, 5.905127],
                [-0.923043, -0.529042, 7.003423],
                [-1.755386, 3.529117, 4.327696],
                [-2.632589, 3.713828, 4.364629],
                [-3.388062, 3.721976, 4.309028],
                [-4.075766, 3.675413, 4.076063],
                [-4.622910, 3.474691, 3.646321],
                [-5.171755, 2.535753, 2.670867],
                [-7.297331, 0.763172, -0.048769],
                [-4.706828, 1.651000, 3.109532],
                [-4.071712, 1.476821, 3.476944],
                [-3.269817, 1.470659, 3.731945],
                [-2.527572, 1.617311, 3.865444],
                [-1.970894, 1.858505, 3.961782],
                [-1.579543, 2.097941, 4.084996],
                [-7.664182, 0.673132, -2.435867],
                [-1.397041, -1.340139, 5.630378],
                [-0.884838, 0.658740, 6.233232],
                [-0.767097, -0.968035, 7.077932],
                [-0.460213, -1.334106, 6.787447],
                [-0.748618, -1.067994, 6.798303],
                [-1.236408, -1.585568, 5.480490],
                [-0.387306, -1.409990, 6.957705],
                [-0.319925, -1.607931, 6.508676],
                [-1.639633, 2.556298, 3.863736],
                [-1.255645, 2.467144, 4.203800],
                [-1.031362, 2.382663, 4.615849],
                [-4.253081, 2.772296, 3.315305],
                [-4.530000, 2.910000, 3.339685],
                [0.463928, 0.955357, 6.633583],
                [4.253081, 2.577646, 3.279702],
                [0.416106, -1.466449, 6.447657],
                [7.087960, 5.434801, 0.099620],
                [2.628639, 2.035898, 3.848121],
                [3.198363, 1.985815, 3.796952],
                [3.775151, 2.039402, 3.646194],
                [4.465819, 2.422950, 3.155168],
                [2.164289, 2.189867, 3.851822],
                [3.208229, 3.223926, 4.115822],
                [2.673803, 3.205337, 4.092203],
                [3.745193, 3.165286, 3.972409],
                [4.161018, 3.059069, 3.719554],
                [5.062006, 1.934418, 2.776093],
                [2.266659, -7.425768, 4.389812],
                [4.445859, 2.663991, 3.173422],
                [7.214530, 2.263009, 0.073150],
                [5.799793, 2.349546, 2.204059],
                [2.844939, -0.720868, 4.433130],
                [0.711452, -3.329355, 5.877044],
                [0.606033, -3.924562, 5.444923],
                [1.431615, -3.500953, 5.496189],
                [1.914910, -3.803146, 5.028930],
                [1.131043, -3.973937, 5.189648],
                [1.563548, -4.082763, 4.842263],
                [2.650112, -5.003649, 4.188483],
                [0.427049, -1.094134, 7.360529],
                [0.496396, -0.475659, 7.440358],
                [5.253307, 3.881582, 3.363159],
                [1.718698, 0.974609, 4.558359],
                [1.608635, -0.942516, 5.814193],
                [1.651267, -0.610868, 5.581319],
                [4.765501, -0.701554, 3.534632],
                [0.478306, 0.295766, 7.101013],
                [3.734964, 4.508230, 4.550454],
                [4.588603, 4.302037, 4.048484],
                [6.279331, 6.615427, 1.425850],
                [1.220941, 4.142165, 5.106035],
                [2.193489, 3.100317, 4.000575],
                [3.102642, -4.352984, 4.095905],
                [6.719682, -4.788645, -1.745401],
                [1.193824, -1.306795, 5.737747],
                [0.729766, -1.593712, 5.833208],
                [2.456206, -4.342621, 4.283884],
                [2.204823, -4.304508, 4.162499],
                [4.985894, 4.802461, 3.751977],
                [1.592294, -1.257709, 5.456949],
                [2.644548, 4.524654, 4.921559],
                [2.760292, 5.100971, 5.015990],
                [3.523964, 8.005976, 3.729163],
                [5.599763, 5.715470, 2.724259],
                [3.063932, 6.566144, 4.529981],
                [5.720968, 4.254584, 2.830852],
                [6.374393, 4.785590, 1.591691],
                [0.672728, -3.688016, 5.737804],
                [1.262560, -3.787691, 5.417779],
                [1.732553, -3.952767, 5.000579],
                [1.043625, -1.464973, 5.662455],
                [2.321234, -4.329069, 4.258156],
                [2.056846, -4.477671, 4.520883],
                [2.153084, -4.276322, 4.038093],
                [0.946874, -1.035249, 6.512274],
                [1.469132, -4.036351, 4.604908],
                [1.024340, -3.989851, 4.926693],
                [0.533422, -3.993222, 5.138202],
                [0.769720, -6.095394, 4.985883],
                [0.699606, -5.291850, 5.448304],
                [0.669687, -4.949770, 5.509612],
                [0.630947, -4.695101, 5.449371],
                [0.583218, -4.517982, 5.339869],
                [1.537170, -4.423206, 4.745470],
                [1.615600, -4.475942, 4.813632],
                [1.729053, -4.618680, 4.854463],
                [1.838624, -4.828746, 4.823737],
                [2.368250, -3.106237, 4.868096],
                [7.542244, -1.049282, -2.431321],
                [1.826614, -4.399531, 4.399021],
                [1.929558, -4.411831, 4.497052],
                [0.597442, -2.013686, 5.866456],
                [1.405627, -1.714196, 5.241087],
                [0.662449, -1.819321, 5.863759],
                [2.342340, 0.572222, 4.294303],
                [3.327324, 0.104863, 4.113860],
                [1.726175, -0.919165, 5.273355],
                [5.133204, 7.485602, 2.660442],
                [4.538641, 6.319907, 3.683424],
                [3.986562, 5.109487, 4.466315],
                [2.169681, -5.440433, 4.455874],
                [1.395634, 5.011963, 5.316032],
                [1.619500, 6.599217, 4.921106],
                [1.891399, 8.236377, 4.274997],
                [4.195832, 2.235205, 3.375099],
                [5.733342, 1.411738, 2.431726],
                [1.859887, 2.355757, 3.843181],
                [4.988612, 3.074654, 3.083858],
                [1.303263, 1.416453, 4.831091],
                [1.305757, -0.672779, 6.415959],
                [6.465170, 0.937119, 1.689873],
                [5.258659, 0.945811, 2.974312],
                [4.432338, 0.722096, 3.522615],
                [3.300681, 0.861641, 3.872784],
                [2.430178, 1.131492, 4.039035],
                [1.820731, 1.467954, 4.224124],
                [0.563221, 2.307693, 5.566789],
                [6.338145, -0.529279, 1.881175],
                [5.587698, 3.208071, 2.687839],
                [0.242624, -1.462857, 7.071491],
                [1.611251, 0.339326, 4.895421],
                [7.743095, 2.364999, -2.005167],
                [1.391142, 1.851048, 4.448999],
                [1.785794, -0.978284, 4.850470],
                [4.670959, 2.664461, 3.084075],
                [1.333970, -0.283761, 6.097047],
                [7.270895, -2.890917, -2.252455],
                [1.856432, 2.585245, 3.757904],
                [0.923388, 0.073076, 6.671944],
                [5.000589, -6.135128, 1.892523],
                [5.085276, -7.178590, 0.714711],
                [7.159291, -0.811820, -0.072044],
                [5.843051, -5.248023, 0.924091],
                [6.847258, 3.662916, 0.724695],
                [2.412942, -8.258853, 4.119213],
                [0.179909, -1.689864, 6.573301],
                [2.103655, -0.163946, 4.566119],
                [6.407571, 2.236021, 1.560843],
                [3.670075, 2.360153, 3.635230],
                [3.177186, 2.294265, 3.775704],
                [2.196121, -4.598322, 4.479786],
                [6.234883, -1.944430, 1.663542],
                [1.292924, -9.295920, 4.094063],
                [3.210651, -8.533278, 2.802001],
                [4.068926, -7.993109, 1.925119],
                [2.724032, 2.315802, 3.777151],
                [2.288460, 2.398891, 3.697603],
                [1.998311, 2.496547, 3.689148],
                [6.130040, 3.399261, 2.038516],
                [2.288460, 2.886504, 3.775031],
                [2.724032, 2.961810, 3.871767],
                [3.177186, 2.964136, 3.876973],
                [3.670075, 2.927714, 3.724325],
                [4.018389, 2.857357, 3.482983],
                [7.555811, 4.106811, -0.991917],
                [4.018389, 2.483695, 3.440898],
                [1.776217, -2.683946, 5.213116],
                [1.222237, -1.182444, 5.952465],
                [0.731493, -2.536683, 5.815343],
                [4.135272, -6.996638, 2.671970],
                [3.311811, -7.660815, 3.382963],
                [1.313701, -8.639995, 4.702456],
                [5.940524, -6.223629, -0.631468],
                [1.998311, 2.743838, 3.744030],
                [0.901447, 1.236992, 5.754256],
                [2.308977, -8.974196, 3.609070],
                [6.954154, -2.439843, -0.131163],
                [1.098819, -4.458788, 5.120727],
                [1.181124, -4.579996, 5.189564],
                [1.255818, -4.787901, 5.237051],
                [1.325085, -5.106507, 5.205010],
                [1.546388, -5.819392, 4.757893],
                [1.953754, -4.183892, 4.431713],
                [2.117802, -4.137093, 4.555096],
                [2.285339, -4.051196, 4.582438],
                [2.850160, -3.665720, 4.484994],
                [5.278538, -2.238942, 2.861224],
                [0.946709, 1.907628, 5.196779],
                [1.314173, 3.104912, 4.231404],
                [1.780000, 2.860000, 3.881555],
                [1.845110, -4.098880, 4.247264],
                [5.436187, -4.030482, 2.109852],
                [0.766444, 3.182131, 4.861453],
                [1.938616, -6.614410, 4.521085],
                [0.516573, 1.583572, 6.148363],
                [1.246815, 0.230297, 5.681036],
                [0.997827, -6.930921, 4.979576],
                [3.288807, -5.382514, 3.795752],
                [2.311631, -1.566237, 4.590085],
                [2.680250, -6.111567, 4.096152],
                [3.832928, -1.537326, 4.137731],
                [2.961860, -2.274215, 4.440943],
                [4.386901, -2.683286, 3.643886],
                [1.217295, -7.834465, 4.969286],
                [1.542374, -0.136843, 5.201008],
                [3.878377, -6.041764, 3.311079],
                [3.084037, -6.809842, 3.814195],
                [3.747321, -4.503545, 3.726453],
                [6.094129, -3.205991, 1.473482],
                [4.588995, -4.728726, 2.983221],
                [6.583231, -3.941269, 0.070268],
                [3.492580, -3.195820, 4.130198],
                [1.255543, 0.802341, 5.307551],
                [1.126122, -0.933602, 6.538785],
                [1.443109, -1.142774, 5.905127],
                [0.923043, -0.529042, 7.003423],
                [1.755386, 3.529117, 4.327696],
                [2.632589, 3.713828, 4.364629],
                [3.388062, 3.721976, 4.309028],
                [4.075766, 3.675413, 4.076063],
                [4.622910, 3.474691, 3.646321],
                [5.171755, 2.535753, 2.670867],
                [7.297331, 0.763172, -0.048769],
                [4.706828, 1.651000, 3.109532],
                [4.071712, 1.476821, 3.476944],
                [3.269817, 1.470659, 3.731945],
                [2.527572, 1.617311, 3.865444],
                [1.970894, 1.858505, 3.961782],
                [1.579543, 2.097941, 4.084996],
                [7.664182, 0.673132, -2.435867],
                [1.397041, -1.340139, 5.630378],
                [0.884838, 0.658740, 6.233232],
                [0.767097, -0.968035, 7.077932],
                [0.460213, -1.334106, 6.787447],
                [0.748618, -1.067994, 6.798303],
                [1.236408, -1.585568, 5.480490],
                [0.387306, -1.409990, 6.957705],
                [0.319925, -1.607931, 6.508676],
                [1.639633, 2.556298, 3.863736],
                [1.255645, 2.467144, 4.203800],
                [1.031362, 2.382663, 4.615849],
                [4.253081, 2.772296, 3.315305],
                [4.530000, 2.910000, 3.339685]], dtype=np.float32)

ADJ_MODEL_POINTS = np.array([MODEL_POINTS[i] for i in [10, 54, 284, 9, 8, 122, 351, 68, 208, 152, 164]], dtype=np.float32)

class FaceFeaturesCalculator:
    def __init__(self, frame_size, debug=0):
        self.head_rotation = np.zeros((3, 1))
        self.head_translation = np.zeros((3, 1))
        
        self.camera_matrix = np.array(
            [[frame_size[1], 0, frame_size[1] / 2],
             [0, frame_size[1], frame_size[0] / 2],
             [0, 0, 1]], dtype=np.float64)
        self.dist_co = np.zeros((4, 1), dtype=np.float32)
        
        self.debug = debug
    
    def head(self, frame, lmks, norm_lmks):
        #face_2d = np.array([lmks[i] for i in [10, 54, 284, 9, 8, 122, 351, 68, 208, 152, 164]], dtype=np.float32)

        _, self.head_rotation, self.head_translation = cv2.solvePnP(
                MODEL_POINTS,
                lmks,
                self.camera_matrix,
                self.dist_co,
                rvec=self.head_rotation,
                tvec=self.head_translation,
                useExtrinsicGuess=True, flags=cv2.SOLVEPNP_SQPNP)

        rot_mat = cv2.Rodrigues(self.head_rotation)[0]
        pose_mat = cv2.hconcat((rot_mat, self.head_translation))
        euler = cv2.decomposeProjectionMatrix(pose_mat)[-1]

        if euler[0] < 0:
            euler[0] += 360
        euler[1] *= -1
        euler[2] *= -1

        return frame, euler, self.head_translation

    
    def mouth(self, frame, lmks, norm_lmks):
        m1 = norm_lmks[78]
        m2 = norm_lmks[81]
        m3 = norm_lmks[13]
        m4 = norm_lmks[311]
        m5 = norm_lmks[308]
        m6 = norm_lmks[402]
        m7 = norm_lmks[14]
        m8 = norm_lmks[178]

        mouth_aspect_ratio = np.clip((np.linalg.norm(m2 - m8) + np.linalg.norm(m3 - m7) + np.linalg.norm(m4 - m6)) / (2 * np.linalg.norm(m1 - m5) + 1e-6), 0.0, 1.0)

        left_eye_inner_corner = norm_lmks[133]
        left_eye_outer_corner = norm_lmks[130]
        right_eye_inner_corner = norm_lmks[362]
        right_eye_outer_corner = norm_lmks[263]

        eye_inner_corner_dist = np.linalg.norm(left_eye_inner_corner - right_eye_inner_corner)
        eye_outer_corner_dist = np.linalg.norm(left_eye_outer_corner - right_eye_outer_corner)

        upper_inner_lip = norm_lmks[13]
        lower_inner_lip = norm_lmks[14]
        left_mouth_corner = norm_lmks[61]
        right_mouth_corner = norm_lmks[291]

        raw_mouth_y_amt = np.linalg.norm(upper_inner_lip - lower_inner_lip)
        raw_mouth_x_amt = np.linalg.norm(left_mouth_corner - right_mouth_corner)

        raw_ratio_y = raw_mouth_y_amt / eye_inner_corner_dist
        raw_ratio_x = raw_mouth_x_amt / eye_outer_corner_dist

        ratio_y = remap((raw_ratio_y + mouth_aspect_ratio / 2.0), 0.17, 0.8)
        ratio_x = np.clip((remap(raw_ratio_x, 0.35, 0.9) - 0.4) * 2.2, -0.8, 0.8)

        return frame, (ratio_x, ratio_y)
    
    def eye(self, frame, lmks, norm_lmks):
        left_eye_inner_corner = norm_lmks[133]
        left_eye_outer_corner = norm_lmks[33]
        right_eye_inner_corner = norm_lmks[263]
        right_eye_outer_corner = norm_lmks[362]
        left_eye_lower = norm_lmks[159]
        left_eye_upper = norm_lmks[145]
        right_eye_lower = norm_lmks[386]
        right_eye_upper = norm_lmks[374]

        left_eye_width = np.linalg.norm(left_eye_inner_corner - left_eye_outer_corner)
        right_eye_width = np.linalg.norm(right_eye_inner_corner - right_eye_outer_corner)
        left_eye_height = np.linalg.norm(left_eye_upper - left_eye_lower)
        right_eye_height = np.linalg.norm(right_eye_upper - right_eye_lower)

        left_eye_mid = (left_eye_inner_corner + left_eye_outer_corner + left_eye_lower) / 3.0
        right_eye_mid = (right_eye_inner_corner + right_eye_outer_corner + right_eye_lower) / 3.0
        
        left_iris_center = norm_lmks[468]
        right_iris_center = norm_lmks[473]

        left_iris_ratio_x = (left_iris_center[0] - left_eye_mid[0]) / (left_eye_width / 4.0)
        left_iris_ratio_x = np.clip(left_iris_ratio_x, -1.0, 1.0)
        left_iris_ratio_y = (left_iris_center[1] - left_eye_mid[1]) / (left_eye_height / 5.0)
        left_iris_ratio_y = np.clip(left_iris_ratio_y, -1.0, 1.0)
        
        right_iris_ratio_x = (right_iris_center[0] - right_eye_mid[0]) / (right_eye_width / 4.0)
        right_iris_ratio_x = np.clip(right_iris_ratio_x, -1.0, 1.0)
        right_iris_ratio_y = (right_iris_center[1] - right_eye_mid[1]) / (right_eye_height / 5.0)
        right_iris_ratio_y = np.clip(right_iris_ratio_y, -1.0, 1.0)

        left_eye_ratio = left_eye_width / left_eye_height
        right_eye_ratio = right_eye_width / right_eye_height

        if left_eye_ratio > 3.2:
            left_iris_ratio_x = right_iris_ratio_x
            left_iris_ratio_y = right_iris_ratio_y
        elif right_eye_ratio > 3.2:
            right_iris_ratio_x = left_iris_ratio_x
            right_iris_ratio_y = left_iris_ratio_y
        elif left_eye_ratio > 3.2 and right_eye_ratio > 3.2:
            left_iris_ratio_x = 0.0
            left_iris_ratio_y = 0.0
            right_iris_ratio_x = 0.0
            right_iris_ratio_y = 0.0
        else:
            old_left_iris_ratio_x = left_iris_ratio_x
            old_left_iris_ratio_y = left_iris_ratio_y
            left_iris_ratio_x = lerp(0.2, left_iris_ratio_x, right_iris_ratio_x)
            left_iris_ratio_y = lerp(0.2, left_iris_ratio_y, right_iris_ratio_y)
            right_iris_ratio_x = lerp(0.2, right_iris_ratio_x, old_left_iris_ratio_x)
            right_iris_ratio_y = lerp(0.2, right_iris_ratio_y, old_left_iris_ratio_y)
        
        left_eye_ratio = 1.0 - remap(left_eye_ratio / 6, 0.53, 0.6)
        right_eye_ratio = 1.0 - remap(right_eye_ratio / 6, 0.53, 0.6)

        return frame, (left_iris_ratio_x, left_iris_ratio_y), (right_iris_ratio_x, right_iris_ratio_y), (left_eye_ratio, right_eye_ratio)
    

def remap(x, m, M):
    return (max(m, min(x, M)) - m) / (M - m)


def lerp(c, a, b):
    return ((1 - c) * a) + (c * b)


def get_tri_normal(a, b ,c):
    cb = c - b
    ab = a - b
    cross = np.cross(cb, ab)

    return cross / np.linalg.norm(cross)