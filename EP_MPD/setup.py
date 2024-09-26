from setuptools import setup

setup(
   name='ep_mpd',
   version='1.0.0',
   description='Privacy-preserving Multi-party Data Deduplication',
   author='Vishnu Asutosh Dasu',
   author_email='vdasu@psu.edu',
   packages=['ep_mpd', 'ep_mpd.eg_psi', 'ep_mpd.eg_psi.type1', 'ep_mpd.eg_psi.type2'],
   install_requires=['cryptography', 'oprf'],
)
