import json
import re
import jieba
from pypinyin import Style, lazy_pinyin  # 同音字识别
import pyperclip  # 按格式复制到剪贴板

# 处理前要被删除的字符 - [会影响分词结果和识别结果的字词]
black_list_pre = []
# 处理后要删除的字符 -  [不影响分词结果和识别结果的字词，只是为了加快处理速度]
black_list_lte = []
# 省份简称
provice_list = ['京', '津', '沪', '渝', '冀', '豫', '云', '辽', '黑', '湘', '皖', '鲁', '新', '苏',
                '浙', '赣', '鄂', '桂', '甘', '晋', '蒙', '陕', '吉', '闽', '贵', '粤', '青', '藏', '川', '宁', '琼']
# 百家姓 修改版
first_name_list = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄', '危', '江', '童', '颜', '郭', '梅', '盛', '林', '刁', '钟', '徐', '邱', '骆', '高', '夏', '蔡', '田', '樊', '胡', '凌', '霍', '虞', '万', '支', '柯', '昝', '管', '卢', '莫', '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣', '贲', '邓', '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆', '荣', '翁', '荀', '羊', '於', '惠', '甄', '曲', '家', '封', '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫', '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲', '伊', '宫', '宁', '仇', '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘', '景', '詹', '束', '龙',
                   '叶', '幸', '司', '韶', '郜', '付', '菅', '黎', '蓟', '肖', '薄', '印', '宿', '白', '怀', '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙', '池', '乔', '阴', '胥', '能', '苍', '双', '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬', '申', '扶', '堵', '冉', '宰', '郦', '雍', '郤', '璩', '桑', '桂', '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '郏', '浦', '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', '茹', '习', '宦', '艾', '鱼', '容', '向', '古', '易', '慎', '戈', '廖', '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文', '寇', '广', '禄', '阙', '东', '欧', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾', '辛', '阚', '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '後', '荆', '红', '游', '竺', '权', '逯', '盖', '益', '桓', '公', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', '赫连', '皇甫', '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐', '钟离', '宇文', '长孙', '慕容', '鲜于', '闾丘', '司徒', '司空', '亓官', '司寇', '仉', '督', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正', '壤驷', '公良', '拓跋', '夹谷', '宰父', '谷梁', '晋', '楚', '闫', '法', '汝', '鄢', '涂', '钦', '段干', '百里', '东郭', '南门', '呼延', '归', '海', '羊舌', '微生', '岳', '帅', '缑', '亢', '况', '后', '有', '琴', '梁丘', '左丘', '东门', '西门', '商', '牟', '佘', '佴', '伯', '赏', '南宫', '墨', '哈', '谯', '笪', '年', '爱', '阳', '佟', '第五', '言', '福']
# 错别字列表
typo_list = [("卾", "鄂"), ("Ⅹ", "X")]

# “名” 正则
name_pattern = r"([\u4e00-\u9fa5]{1,2})"

client_list = []
error_list = []


class client:
    # 定义 客户 类
    def __init__(self, name=None, tel=None, license=None):
        self.name = name
        self.tel = tel
        self.license = license

    def __str__(self):
        return "name: {}, tel: {}, license: {}".format(self.name, self.tel, self.license)

    def __dict__(self):
        return {'name': self.name, 'tel': self.tel, 'license': self.license}

    def __format__(self):
        if self.name is None:
            self.name = ''
        if self.tel is None:
            self.tel = ''
        # 自定义复制格式
        return f"{self.name}\t{i.tel}\t\t{i.license}"

    def set_name(self, name):
        if self.name is None:
            self.name = name
            return self
        else:
            client_list.append(self)
            print(self)
            return client(name=name)

    def set_tel(self, tel):
        if self.tel is None:
            self.tel = tel
            return self
        else:
            client_list.append(self)
            print(self)
            return client(tel=tel)

    def set_license(self, license):
        if self.license is None:
            self.license = license
            return self
        else:
            client_list.append(self)
            print(self)
            return client(license=license)


class Encoder(json.JSONEncoder):
    # 处理自定义类的json转换
    def default(self, obj):
        if isinstance(obj, client):
            return obj.__dict__()
        else:
            return json.JSONEncoder.default(self, obj)


# 待处理的消息放置 info.txt
with open("info.txt", "r", encoding="utf-8") as f:
    txt = f.read()
    f.close()

# 在处理前删除要被删除的字符
for i in black_list_pre:
    txt = txt.replace(i, "")

# 错别字替换
for i, j in typo_list:
    txt = txt.replace(i, j)


# 每一个空行为一条消息
txt_split = txt.split("\n\n")

for u, i in enumerate(txt_split):
    jb = list(jieba.cut(i))
    c = client()
    # 人工正则
    for j, v in enumerate(jb):
        if v == '' or v == '\n' or v in black_list_lte:
            # 加快处理速度
            continue
        elif v.isnumeric():
            # 识别手机号和身份证号
            length = len(v)
            if length == 11 and v[0] == '1':
                c = c.set_tel(v)
            elif length == 18:
                # 不需要身份证号码
                pass
        elif v in provice_list:
            # 识别车牌号
            if len(jb[j+1]) == 6:
                # 简称后面一个分词单位是六个字符 则是车牌号
                c = c.set_license(v + jb[j+1].upper())
            elif jb[j+1][0].isalpha() and len(jb[j+1]) != 5:
                # 捡漏 省份简称未被单独分词的情况
                c = c.set_license(v + jb[j+1][:6].upper())
        elif v[0] in first_name_list:
            # 百家姓
            try:
                if re.search(name_pattern, jb[j+1]) is not None and len(v) == 1:
                    c = c.set_name(v + jb[j+1])
                else:
                    c = c.set_name(v)
            except IndexError:
                c = c.set_name(v)
        elif len(v) == 1 and re.search(name_pattern, v) is not None and jb[j-1] == c.name:
            # 捡漏 姓氏未被单独分词的情况
            c.name += v
        elif len(v) == 1 and lazy_pinyin(v[0], style=Style.NORMAL)[0] in ['gan', 'gang']:
            # 错别字拼音识别
            c = c.set_license('赣' + jb[j+1][:6].upper())
        else:
            # 我也无能为力了 人工识别吧
            error_list.append(v)
    if c.license != None:
        # 不需要没有车牌号的客户
        client_list.append(c)
    print(c)

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(client_list, f, ensure_ascii=False, cls=Encoder)
    f.close()

with open("error.json", "w", encoding="utf-8") as f:
    json.dump(error_list, f, ensure_ascii=False)
    f.close()

msg = []
# 获取客户列表
for i in client_list:
    msg.append(i.__format__())
# 复制自定义格式
pyperclip.copy('\n'.join(msg))
