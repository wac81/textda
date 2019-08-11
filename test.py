from textda.data_expansion import data_expansion

print(data_expansion('生活里的惬意，无需等到春暖花开', alpha_ri=0.1, alpha_rs=0))



from textda.youdao_translate import *
dir = './data'
translate_batch(os.path.join(dir, 'train'), batch_num=30)
