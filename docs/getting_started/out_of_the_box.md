# Out of the box

You can use the package straight out of the box by making use of the two in-built Form page types. See the limitations of this approach below.

## EmailFormPage

This Page type inherits from Wagtails __AbstractEmailForm__ page type. 

Example usage:

        from wagtail.core.models import Page        
        class HomePage(Page):
            subpage_types = [
                'wagtail_advanced_form_builder.EmailFormPage',
            ]    
            
The __EmailFormPage__ inherits the <span class='color-red'>to_address</span>, <span class='color-red'>from_address</span>, and <span class='color-red'>subject</span> fields and retains the default underlying __AbstractEmailForm__ 
email sending functionality. Please refer to the [Wagtail FormBuilder documentation](https://docs.wagtail.io/en/latest/reference/contrib/forms/index.html) for more information.             
                 
## FormPage

This Page type inherits from Wagtails __AbstractForm__ page type.  

Example usage:

        from wagtail.core.models import Page                
        class HomePage(Page):
            subpage_types = [
                'wagtail_advanced_form_builder.FormPage',
            ]                  
            
## Limitations

The default functionality may well suffice if the following is true:

* The only content you want on the page is the page title and the form field content. i.e. you want this page to act solely as a form container page.
* You're not adding additional functionality into the default Wagtail __Promote__ or __Settings__ tabs on the page in the CMS.
            
