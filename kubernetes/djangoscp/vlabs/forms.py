from django import forms
from vlabs import Config, AppManager


class VlabsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.namespace = 'test-project'
        self.vlcg = Config()
        self.vlam = AppManager(self.namespace)
        self.market = self.vlcg.getmarket()
        super(VlabsForm, self).__init__(*args, **kwargs)
        self.k = None
        self.nameoftheapp = None

    def createapp(self):
        APP_SEL = ()
        i = []
        a = self.vlcg.getmarket()

        for j in range(0, len(a)):
            i.append(j)
        APP_SEL = zip(tuple(i), tuple(a))
        print(APP_SEL)
        self.fields['app'] = forms.ChoiceField(widget=forms.RadioSelect, label='app', choices=APP_SEL)

    def createenv(self, inputvar):
        print(inputvar)
        c = inputvar['appindex']
        del inputvar['appindex']
        for k in inputvar.keys():
            print(k)
            print(inputvar[k])
            self.fields[k] = forms.CharField(label=inputvar[k])
        self.fields['nameoftheapp'] = forms.CharField(label='name of the app')
        self.fields['appindex'] = forms.CharField(widget=forms.HiddenInput(), label='appindex', initial=c)

    def deleteapp(self):
        APP_SEL = ()
        i = []
        a = self.vlam.getrunning()
        print(a)
        for j in range(0, len(a)):
            i.append(j)
        APP_SEL = zip(tuple(i), tuple(a))
        print(APP_SEL)
        self.fields['run'] = forms.ChoiceField(widget=forms.RadioSelect, label='run', choices=APP_SEL)
