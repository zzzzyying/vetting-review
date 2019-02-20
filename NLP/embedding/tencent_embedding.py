from gensim.models.word2vec import Word2VecKeyedVectors
wv = Word2VecKeyedVectors.load_word2vec_format("/hd/tecent_ew/Tencent_AILab_ChineseEmbedding.txt", binary=False)

kw = "电话号码"

print kw, "/".join([word for word, sim in wv.most_similar(kw, topn=10)])

#https://www.cnblogs.com/bymo/p/8440722.html
'''
>>> kw = u"电话号码"
>>> print kw, "/".join([word for word, sim in wv.most_similar(kw, topn=10)])
/usr/local/lib/python2.7/dist-packages/gensim/matutils.py:737: FutureWarning: Conversion of the second argument of issubdtype from `int` to `np.signedinteger` is deprecated. In future, it will be treated as `np.int64 == np.dtype(int).type`.
  if np.issubdtype(vec.dtype, np.int):
电话号码 手机号码/手机号/电话号/座机号码/你的电话号码/联系号码/几个电话号码/座机号/电话/新号码
>>> print kw, "/".join([word for word, sim in wv.most_similar(kw, topn=100)])
电话号码 手机号码/手机号/电话号/座机号码/你的电话号码/联系号码/几个电话号码/座机号/电话/新号码/电话拨打/我的电话/私人号码/联系方式/家里的电话号码/电话信息/个人电话/手机通讯录/通话记录/手机电话/联系人电话/你的手机号/qq号码/家庭地址/办公电话/银行账号/电话记录/你的电话/银行卡号/联络方式/固定电话号码/电话本/短信内容/电话簿/电子邮箱地址/家庭电话/移动电话号码/通讯号码/号码显示/私人手机/父母的电话/姓名地址/卡号/办公室电话/短信/住址/私人电话/银行卡号码/电话薄/拨通/电子邮件地址/陌生号码/号码/qq号/其他联系方式/一串数字/住宅电话/显示号码/两个电话/回拨电话/短信信息/单位电话/手机联系人/家庭号码/拨通电话/联系电话号码/通信录/微信号码/通讯录/家庭住址/联系人姓名/联系人的姓名/常用号码/电话和短信/银行卡账号/手机拨打/短信息/拨打/座机电话号码/详细住址/银行卡密码/银行卡卡号/手机电话号码/办公室号码/信用卡号/座机电话/身份证信息/通讯记录/公用电话/通讯簿/留电话/打电话/收到的短信/空号/网络联系方式/骚扰电话/查号码/联络电话/电话通讯录/email地址
>>> kw = u"短信"
>>> print kw, "/".join([word for word, sim in wv.most_similar(kw, topn=100)])
短信 短息/短信息/一条短信/短信内容/电话和短信/手机短信/微信信息/微信消息/陌生号码/短信里/收到短信/短信回复/诈骗短信/陌生短信/通知短信/短信发送/群发短信/qq信息/打开短信/短信提醒/验证码短信/匿名短信/短信信息/qq消息/短消息/回复短信/垃圾短信/一条信息/发信息/骚扰短信/我的短信/手机号码/广告短信/信息回复/电话/语音留言/发送短信/收到的短信/回复信息/发短息/10086/问候短信/扣费短信/电话信息/群发/群发信息/qq留言/祝福短信/短信轰炸/语音电话/微信提醒/祝福信息/邮件/手机信息/微信短信/条微信/发短信/彩信/语音消息/短信提示/电话号码/那条短信/骗子短信/语音信息/信息提醒/转账信息/手机号/推送消息/看短信/骚扰电话/所有短信/短讯/电子邮件/以及短信/电话短信/我的电话/打电话/短信或电话/发消息/手机短信息/通讯录好友/发送失败/短信通知/短信电话/手机里/一则短信/陌生来电/微信发/陌生电话/道歉短信/接到的电话/短信消息/电话或短信/诈骗电话/回短信/未知号码/短信显示/未读信息/诈骗信息/新号码
'''