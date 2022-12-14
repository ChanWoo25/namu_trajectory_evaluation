import numpy as np
import torch
from typing import Tuple

import os
import sys
# print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Rotation import Rotation
from Translation import Translation

class Pose:
    """
        Class for Pose parameterizion.  This can be one of [SE3, se3].
        - if SE3, shape must be [n, 4, 4] or [4, 4]
        - if se3, shape must be [n, 6] or [6]
        - #TODO, But single comparision is yet fully supported.
        Notation
        - T: normally means tranformation (t & R)
        - t: normally means translation
        - R: normally means rotation
        - c: normally means scale factor
    """
    def __init__(self,  t_data:torch.Tensor,
                        R_data:torch.Tensor,
                        R_type:str,
                        R_qtype:str=None) -> None:
        assert (type(t_data) is torch.Tensor), ('t_data type must be torch.Tensor')
        assert (type(R_data) is torch.Tensor), ('R_data type must be torch.Tensor')
        assert (t_data.shape[0] == R_data.shape[0]), ('t and R must be same length')

        self.t_data:Translation = Translation(t_data)
        self.R_data:Rotation    = Rotation(R_data, R_type, R_qtype)
        self.cudable:bool = torch.cuda.is_available()

    @property
    def length(self):
        assert (self.t_data.length == self.R_data.length), 'translation and rotation data should have same length!'
        return self.t_data.length

    def numpy(self, out_Rtype:str) -> Tuple[np.ndarray, np.ndarray, str]:
        if out_Rtype == 'SO3':
            self.R_data = self.R_data.SO3()
        elif out_Rtype == 'so3':
            self.R_data = self.R_data.so3()
        if out_Rtype == 'quat':
            self.R_data = self.R_data.quat()
        else:
            raise AssertionError('Unvalid rotation type!')

        t = self.t_data.numpy()
        R, R_type = self.R_data.numpy()
        return t, R, R_type

    def SE3(self):
        raise NotImplementedError

    def se3(self):
        raise NotImplementedError

if __name__ == '__main__':
    data = torch.randn((2, 3))
    w = Rotation(data, 'so3')
    print(w.data)
