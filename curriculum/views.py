from django.views import generic
from .models import Offering
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

class IndexView(generic.ListView):
    template_name = 'curriculum/index.html'

    def get_queryset(self):
        return Offering.objects.all()

class DetailView(generic.DetailView):
    model = Offering
    template_name = 'curriculum/detail.html'

class OfferingCreate(CreateView):
    model = Offering
    fields = ['course_caution','course_name','course_delivery','course_type','parent_code','strand','department','location','qual_aim','fee_comments','start_date','end_date','start_time','end_time','day','study_year','study_year_duration','wk_hrs','number_wks','glh','number_grps','min_students','max_students','mkt_course_name','mkt_course_overview','mkt_prospectus','mkt_entry_req','mkt_topics','mkt_target','mkt_learning','mkt_assess','mkt_career','mkt_funding','mkt_add_costs','mkt_where','mkt_bring','mkt_other','mkt_tutor',]

class OfferingUpdate(UpdateView):
    model = Offering
    fields = ['course_caution','course_name','course_delivery','course_type','parent_code','strand','department','location','qual_aim','fee_comments','start_date','end_date','start_time','end_time','day','study_year','study_year_duration','wk_hrs','number_wks','glh','number_grps','min_students','max_students','mkt_course_name','mkt_course_overview','mkt_prospectus','mkt_entry_req','mkt_topics','mkt_target','mkt_learning','mkt_assess','mkt_career','mkt_funding','mkt_add_costs','mkt_where','mkt_bring','mkt_other','mkt_tutor',]

class MarketingUpdate(UpdateView):
    model = Offering
    fields = ['mkt_course_name','mkt_course_overview','mkt_prospectus','mkt_entry_req','mkt_topics','mkt_target','mkt_learning','mkt_assess','mkt_career','mkt_funding','mkt_add_costs','mkt_where','mkt_bring','mkt_other','mkt_tutor',]

class OfferingDelete(DeleteView):
    model = Offering
    success_url = reverse_lazy('curriculum:index')
