import os
import sys

#add modules to sys path
if 'QUANT_EXCAHNGE_MODULE_PATH' in os.environ:
  module_path = os.environ['QUANT_EXCAHNGE_MODULE_PATH']
else:
  module_path = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                             "modules")

if not os.path.exists(module_path):
  raise ValueError(f'invalid quant exchange module path:{module_path}')

if 'VIPDOC_PATH' in os.environ:
  vipdoc_path = os.environ['VIPDOC_PATH']
else:
  vipdoc_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                             "vip", "vipdoc")

  if not os.path.exists(vipdoc_path):
    vipdoc_path = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                               "vip", "vipdoc")

if not os.path.exists(vipdoc_path):
  raise ValueError(f'invalid vipdoc path:{vipdoc_path}')

if 'QUANT_EXCAHNGE_DATA_PATH' in os.environ:
  data_path = os.environ['QUANT_EXCAHNGE_DATA_PATH']
else:
  data_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")

if not os.path.exists(data_path):
  raise ValueError(f'invalid quant exchange data path:{data_path}')

sys.path.append(module_path)
sys.dont_write_bytecode = True
