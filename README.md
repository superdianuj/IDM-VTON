
<h1>IDM-VTON: Trying on Garments on Image of Person directly from Shopping Site URL </h1>


## Setup

```bash
git clone --recursive https://github.com/superdianuj/IDM-VTON.git
cd IDM-VTON

conda env create -f environment.yaml
conda activate idm
```

## Inference

```bash
python convert_url_2_img.py --url <link to Amazon website of garment product>
python try_on.py --image_path <path to image on why garment is to be tried on>
```


![image](https://github.com/superdianuj/IDM-VTON/assets/47445756/aea343f4-f9d9-4180-93ca-779b2192e2f3)


In case the try_on.py due to hardware limitations, then use hugging face demo: <a href='https://huggingface.co/spaces/yisol/IDM-VTON'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Demo-yellow'></a>


## Citation
```
@article{choi2024improving,
  title={Improving Diffusion Models for Virtual Try-on},
  author={Choi, Yisol and Kwak, Sangkyung and Lee, Kyungmin and Choi, Hyungwon and Shin, Jinwoo},
  journal={arXiv preprint arXiv:2403.05139},
  year={2024}
}
```



## License
The codes and checkpoints in this repository are under the [CC BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).


