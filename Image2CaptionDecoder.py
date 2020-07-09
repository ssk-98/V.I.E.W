import chainer
import chainer.functions as F
import chainer.links as L

class Image2CaptionDecoder(chainer.Chain):
    def __init__(self, vocaburary_size, img_feature_dim=2048, hidden_dim=512,dropout_ratio=0.5,train=True, n_layers=1):
        super(Image2CaptionDecoder, self).__init__(
            embed_word=  L.EmbedID(vocaburary_size, hidden_dim),
            embed_image= L.Linear(img_feature_dim, hidden_dim),
            lstm = L.NStepLSTM(n_layers=n_layers,in_size=hidden_dim,out_size=hidden_dim,dropout=dropout_ratio),
            decode_word = L.Linear(hidden_dim, vocaburary_size),
        )
        self.dropout_ratio = dropout_ratio
        self.train = train
        self.n_layers=n_layers
        self.hidden_dim=hidden_dim

    def input_cnn_feature(self,hx,cx,image_feature):
        h = self.embed_image(image_feature)
        h = [F.reshape(img_embedding,(1,self.hidden_dim)) for img_embedding in h]#一回　python list/tuple にしないとerrorが出る
        hy, cy, ys  = self.lstm(hx, cx, h, train=self.train)
        return hy,cy

    def __call__(self, hx, cx, caption_batch):
        #hx (~chainer.Variable): Initial hidden states.
        #cx (~chainer.Variable): Initial cell states.
        #xs (list of ~chianer.Variable): List of input sequences.Each element ``xs[i]`` is a :class:`chainer.Variable` holding a sequence.
        xs = [self.embed_word(caption) for caption in caption_batch]
        hy, cy, ys  = self.lstm(hx, cx, xs, train=self.train)
        predicted_caption_batch = [self.decode_word(generated_caption) for generated_caption in ys]
        if self.train:
            loss=0
            for y, t in zip(predicted_caption_batch, caption_batch):
                loss+=F.softmax_cross_entropy(y[0:-1], t[1:])
            return loss/len(predicted_caption_batch)
        else:
            return hy, cy, predicted_caption_batch
