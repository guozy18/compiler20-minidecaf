"""minidecaf 是个包所以使用相对 import，注意下面 main 之前的句点。"""
import sys
from .main import main

sys.exit(main())
