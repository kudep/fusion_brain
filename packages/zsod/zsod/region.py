class Region:
    def __init__(self, l, u, r, d, im_w=300, im_h=300):
        self.l = float(l)
        self.u = float(u)
        self.r = float(max(l, r))
        self.d = float(max(u, d))
        self.im_h = im_h
        self.im_w = im_w
        self.probability = 0.0
        self.idx = 0
        self.label = ""

    def resize(self, im_w, im_h):
        h_ratio = im_h / self.im_h
        w_ratio = im_w / self.im_w
        self.l *= w_ratio
        self.r *= w_ratio
        self.u *= h_ratio
        self.d *= h_ratio
        self.im_w = im_w
        self.im_h = im_h

    def unwrap(self):
        return self.l, self.u, self.r, self.d

    def to_xywh(self):
        return self.l, self.u, self.r - self.l, self.d - self.u

    def intersect(self, other):
        return Region(max(self.l, other.l),
                      max(self.u, other.u),
                      min(self.r, other.r),
                      min(self.d, other.d))

    def area(self):
        return (self.r - self.l) * (self.d - self.u)
