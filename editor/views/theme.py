#Copyright 2014 Newcastle University
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from django.views import generic
from django.core.urlresolvers import reverse

from editor.models import Theme
from editor.forms import NewThemeForm, UpdateThemeForm
from editor.views.generic import AuthorRequiredMixin

class CreateView(generic.CreateView):
    """ Create a theme """

    model = Theme
    form_class = NewThemeForm
    template_name = 'theme/create.html'

    def get_form_kwargs(self):
        kwargs = super(CreateView,self).get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('theme_list')

class UpdateView(AuthorRequiredMixin,generic.UpdateView):
	""" Edit a theme """

	model = Theme
	form_class = UpdateThemeForm
	template_name = 'theme/edit.html'

	def get_success_url(self):
		return reverse('theme_list')

class ListView(generic.ListView):
    """ List all the current user's themes """
    
    model = Theme
    template_name = 'theme/list.html'

    def get_queryset(self):
        return Theme.objects.filter(author=self.request.user)

class DeleteView(AuthorRequiredMixin,generic.DeleteView):
    model = Theme
    template_name = 'theme/delete.html'

    def get_success_url(self):
        return reverse('theme_list')
