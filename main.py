from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

#настройки на счет фиксации окна
#и его высоты и ширины
from kivy.config import Config
Config.set('graphics', 'resizeable', 0);
Config.set('graphics', 'width', 480);
Config.set('graphics', 'height', 640);

#для позиционирования
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout

class ChatApp(App):
	def build(self):

		# fl = FloatLayout(size = (300, 300))
		al = AnchorLayout()
		bl = BoxLayout(orientation = 'vertical', padding=25, size_hint = [None, None], size=[300, 200])

		gr = GridLayout(cols=2, spacing=3)

		self.new_comment_wrap = BoxLayout(orientation = 'vertical')
		bl.add_widget(self.new_comment_wrap)


		# которые есть комментарии
		comment = GridLayout(cols=2, spacing=3)
		comment.add_widget( Label( text="You", font_size=14 ) )
		comment.add_widget( Label( text="Message", font_size=14 ) )
		bl.add_widget(comment)



		gr.add_widget( Label( text="You", font_size=14 ) )
		gr.add_widget( TextInput(  ) )

		bl.add_widget(gr)

		# пустой виджет
		bl.add_widget( Widget() )

		bl.add_widget(
			Button(
				text = "Btn",
				font_size = 16,
				on_press = self.btn_press,
				background_color = [.32, .85, .94, 1],
				background_normal = '',
				size_hint = (.5, .25),
				pos = (640 / 2 - 160, 480 / 2 - (480 * .25 / 2 ))
			)
		)


		al.add_widget(bl)

		return al

	def btn_press(self, instance):
		print('Btn press')
		instance.text = "Я нажата"
		# которые будут комментарии
		comment = GridLayout(cols=2, spacing=3, padding=10)
		comment.add_widget( Label( text="You", font_size=14 ) )
		comment.add_widget( Label( text="Message", font_size=14 ) )
		self.new_comment_wrap.add_widget(comment)

if __name__ == "__main__":
	ChatApp().run()