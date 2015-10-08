from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from scripts.models import ConfigTemplate
from scripts.models import ConfigTemplateForm

from scripts.models import Script
from scripts.models import ScriptForm


def index(request):
    template_list = ConfigTemplate.objects.all().order_by('modified')
    script_list = Script.objects.all().order_by('modified')
    context = {'template_list': template_list, 'script_list': script_list}
    return render(request, 'configTemplates/index.html', context)


def new_template(request):
    template_form = ConfigTemplateForm()
    context = {'template_form': template_form}
    return render(request, 'configTemplates/new.html', context)


def edit(request, template_id):
    template = get_object_or_404(ConfigTemplate, pk=template_id)
    template_form = ConfigTemplateForm(instance=template)
    context = {'template_form': template_form, 'template': template}
    return render(request, 'configTemplates/edit.html', context)


def update(request):
    try:
        if "id" in request.POST:
            template_id = request.POST['id']
            template = get_object_or_404(ConfigTemplate, pk=template_id)
            template.name = request.POST['name']
            template.description = request.POST['description']
            template.template= request.POST['template']
            template.save()
            return HttpResponseRedirect('/scripts')
        else:
            return render(request, 'error.html', {
                'error_message': "Invalid data in POST"
            })

    except KeyError:
        return render(request, 'error.html', {
            'error_message': "Invalid data in POST"
        })


def create(request):
    template_form = ConfigTemplateForm(request.POST, request.FILES)
    if template_form.is_valid():
        print "Saving form"
        template_form.save()
        return HttpResponseRedirect('/scripts')
    else:
        context = {'error': "Form isn't valid!"}
        return render(request, 'error.html', context)


def detail(request, template_id):
    template = get_object_or_404(ConfigTemplate, pk=template_id)
    return render(request, 'configTemplates/details.html', {'template': template})


def delete(request, template_id):
    template = get_object_or_404(ConfigTemplate, pk=template_id)
    template.delete()
    return HttpResponseRedirect('/scripts')


def error(request):
    context = {'error': "Unknown Error"}
    return render(request, 'error.html', context)


def new_script(request):
    script_form = ScriptForm()
    context = {'script_form': script_form}
    return render(request, 'scripts/new.html', context)


def create_script(request):
    required_fields = set(['name', 'description', 'script'])
    if not required_fields.issubset(request.POST):
        return render(request, 'error.html', {
            'error': "Form isn't valid!"
        })

    # clean up crlf
    script_content = request.POST["script"]
    request.POST["script"] = script_content.replace("\r", "")

    script_form = ScriptForm(request.POST, request.FILES)
    if script_form.is_valid():
        print "Saving form"
        script_form.save()
        return HttpResponseRedirect('/scripts')
    else:
        context = {'error': "Form isn't valid!"}
        return render(request, 'error.html', context)


def view_script(request, script_id):
    script = get_object_or_404(Script, pk=script_id)
    return render(request, 'scripts/details.html', {'script': script})


def edit_script(request, script_id):
    script = get_object_or_404(Script, pk=script_id)
    script_form = ScriptForm(instance=script)
    context = {'script_form': script_form, 'script': script}
    return render(request, 'scripts/edit.html', context)


def update_script(request):
    required_fields = set(['id', 'name', 'description', 'script'])
    if not required_fields.issubset(request.POST):
        return render(request, 'scripts/error.html', {
            'error_message': "Invalid data in POST"
        })
    try:
        if "id" in request.POST:
            script_id = request.POST['id']
            script = get_object_or_404(Script, pk=script_id)
            script.name = request.POST['name']
            script.description = request.POST['description']
            script.script = request.POST['script'].replace("\r", "")
            script.save()
            return HttpResponseRedirect('/scripts')
        else:
            return render(request, 'scripts/error.html', {
                'error_message': "Invalid data in POST"
            })

    except Exception as e:
        print str(e)
        return render(request, 'scripts/error.html', {
            'error_message': 'Could not update script!'
        })
    
    
def delete_script(request, script_id):
    script = get_object_or_404(Script, pk=script_id)
    script.delete()
    return HttpResponseRedirect('/scripts')