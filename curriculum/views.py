from django.views import generic
from .models import Offering, Lars
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render_to_response

class IndexView(generic.ListView):
    template_name = 'curriculum/index.html'

    def get_queryset(self):
        return Offering.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['drafts'] = self.get_queryset().filter(course_caution=True)
        context['commits'] = self.get_queryset().filter(course_caution=False)

        return context

class TableView(generic.ListView):
    template_name = 'curriculum/table.html'

    def get_queryset(self):
        return Offering.objects.all()

class HierarchyView(generic.ListView):
    template_name = 'curriculum/hierarchy.html'

    def get_queryset(self):
        return Offering.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HierarchyView, self).get_context_data(**kwargs)
        context['main'] = self.get_queryset().filter(course_type='M')
        context['sub'] = self.get_queryset().filter(parent_code__in=context['main'])
        return context

class DetailView(generic.DetailView):
    model = Offering
    template_name = 'curriculum/detail.html'

class OfferingCreate(CreateView):
    model = Offering
    template_name = 'curriculum/add-form.html'
    fields = ['course_caution','course_name','course_delivery','course_type','parent_code','strand','department','location','qual_aim','fee_comments','start_date','end_date','start_time','end_time','day','study_year','study_year_duration','wk_hrs','number_wks','glh','number_grps','min_students','max_students','mkt_course_name','mkt_course_overview','mkt_prospectus','mkt_entry_req','mkt_topics','mkt_target','mkt_learning','mkt_assess','mkt_career','mkt_add_costs','mkt_where','mkt_bring','mkt_other','mkt_tutor',]

class OfferingUpdate(UpdateView):
    model = Offering
    template_name = 'curriculum/edit-form.html'
    fields = ['course_caution','course_name','course_delivery','course_type','parent_code','strand','department','location','qual_aim','fee_comments','start_date','end_date','start_time','end_time','day','study_year','study_year_duration','wk_hrs','number_wks','glh','number_grps','min_students','max_students','mkt_course_name','mkt_course_overview','mkt_prospectus','mkt_entry_req','mkt_topics','mkt_target','mkt_learning','mkt_assess','mkt_career','mkt_add_costs','mkt_where','mkt_bring','mkt_other','mkt_tutor',]

class MarketingUpdate(UpdateView):
    model = Offering
    fields = ['mkt_course_name','mkt_course_overview','mkt_prospectus','mkt_entry_req','mkt_topics','mkt_target','mkt_learning','mkt_assess','mkt_career','mkt_funding','mkt_add_costs','mkt_where','mkt_bring','mkt_other','mkt_tutor',]

class OfferingDelete(DeleteView):
    model = Offering
    success_url = reverse_lazy('curriculum:table')

def search_lars(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    if search_text == '':
        result = ''
    else:
        result = Lars.objects.filter(qual_aim__icontains=search_text)[:3]

    return render_to_response('curriculum/ajax_search.html', {'lars': result})
