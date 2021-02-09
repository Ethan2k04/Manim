from manimlib.imports import *

class WordEffect(Scene):
    def construct(self):
        word = TextMobject("H","e","l","l","W","o","r","l","d")
        word.scale(2)
        self.play(FadeInFrom(word[0],UP),FadeInFrom(word[1],DOWN),
                  FadeInFrom(word[2],UP),FadeInFrom(word[3],DOWN),
                  FadeInFrom(word[4],UP),FadeInFrom(word[5],DOWN),
                  FadeInFrom(word[6],UP),FadeInFrom(word[7],DOWN),
                  FadeInFrom(word[8],UP))
