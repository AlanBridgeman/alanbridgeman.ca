from wagtail.admin.panels import InlinePanel

from wagtailmenus.models import MenuPage

class PortfolioPage(MenuPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['portfolio.CreativePortfolioPage', 'portfolio.CodingPortfolioPage']