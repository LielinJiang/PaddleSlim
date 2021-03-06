# Copyright (c) 2019  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
sys.path.append('..')
import unittest
import paddle.fluid as fluid
from nas.search_space_factory import SearchSpaceFactory


class TestSearchSpace(unittest.TestCase):
    def test_searchspace(self):
        # if output_size is 1, the model will add fc layer in the end.
        config = {'input_size': 224, 'output_size': 7, 'block_num': 5}
        space = SearchSpaceFactory()

        my_space = space.get_search_space([('MobileNetV2Space', config)])
        model_arch = my_space.token2arch()

        train_prog = fluid.Program()
        startup_prog = fluid.Program()
        with fluid.program_guard(train_prog, startup_prog):
            input_size = config['input_size']
            model_input = fluid.layers.data(
                name='model_in',
                shape=[1, 3, input_size, input_size],
                dtype='float32',
                append_batch_size=False)
            predict = model_arch[0](model_input)
            self.assertTrue(predict.shape[2] == config['output_size'])


class TestMultiSearchSpace(unittest.TestCase):
    space = SearchSpaceFactory()

    config0 = {'input_size': 224, 'output_size': 7, 'block_num': 5}
    config1 = {'input_size': 7, 'output_size': 1, 'block_num': 2}
    my_space = space.get_search_space(
        [('MobileNetV2Space', config0), ('ResNetSpace', config1)])
    model_archs = my_space.token2arch()

    train_prog = fluid.Program()
    startup_prog = fluid.Program()
    with fluid.program_guard(train_prog, startup_prog):
        input_size = config0['input_size']
        model_input = fluid.layers.data(
            name='model_in',
            shape=[1, 3, input_size, input_size],
            dtype='float32',
            append_batch_size=False)
        for model_arch in model_archs:
            predict = model_arch(model_input)
            model_input = predict
        print(predict)


if __name__ == '__main__':
    unittest.main()
