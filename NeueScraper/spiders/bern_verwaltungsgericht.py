# -*- coding: utf-8 -*-
import scrapy
import re
import logging


class BernSpider(scrapy.Spider):
	name = 'bern/verwaltungsgericht'
	allowed_domains = ['www.zsg-entscheide.apps.be.ch']
	start_urls = ['https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/loadTable']
	
	RESULT_PAGE_URL = 'https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/loadTable'
	# Hole immer nur ein Dokument um Probleme mit Deduplizierung und unterschiedlichen Reihenfolgen zu verringern
	RESULT_QUERY_TPL = r'''7|0|67|https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/|9012D0DA9E934A747A7FE70ABB27518D|tribunavtplus.client.zugriff.LoadTableService|search|java.lang.String/2004016611|java.util.ArrayList/4159755760|Z|I|java.util.Map||0|OG|BM|BJS|EO|O|0;false|5;true|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Thesaurus\\suisse.fts|1|java.util.HashMap/1797211028|reportpath|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Reports\\ExportResults.jasper|viewtype|2|reporttitle|reportexportpath|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Reports\\Export_1592254990808|reportname|Export_1592254990808|decisionDate|Entscheiddatum|dossierNumber|Dossier|classification|Zusatzeigenschaft|indexCode|Quelle|dossierObject|Betreff|law|Rechtsgebiet|shortText|Vorschautext|department|Gericht|createDate|Erfasst am|creater|Ersteller|judge|Richter|executiontype|Erledigungsart|legalDate|Rechtskraftdatum|objecttype|Objekttyp|typist|Schreiber|description|Beschreibung|reference|Referenz|relevance|Relevanz|de|1|2|3|4|41|5|5|6|7|6|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|8|8|5|5|5|5|7|9|9|5|5|5|5|5|5|5|10|11|6|0|0|6|5|5|12|5|13|5|14|5|15|5|16|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|1|{page_nr}|17|18|19|20|0|21|5|5|22|5|23|5|24|5|25|5|26|5|10|5|27|5|28|5|29|5|30|21|18|5|31|5|32|5|33|5|34|5|35|5|36|5|37|5|38|5|39|5|40|5|41|5|42|5|43|5|44|5|45|5|46|5|47|5|48|5|49|5|50|5|51|5|52|5|53|5|54|5|55|5|56|5|57|5|58|5|59|5|60|5|61|5|62|5|63|5|64|5|65|5|66|10|67|10|10|11|11|0|'''
	RESULT_QUERY_TPL_AB = r'''7|0|68|https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/|9012D0DA9E934A747A7FE70ABB27518D|tribunavtplus.client.zugriff.LoadTableService|search|java.lang.String/2004016611|java.util.ArrayList/4159755760|Z|I|java.util.Map||0|OG|BM|BJS|EO|O|{datum}|0;false|5;true|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Thesaurus\\suisse.fts|1|java.util.HashMap/1797211028|reportpath|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Reports\\ExportResults.jasper|viewtype|2|reporttitle|reportexportpath|E:\\webapps\\a2y\\a2ya-www-trbpub100web\\Reports\\Export_1595357657961|reportname|Export_1595357657961|decisionDate|Entscheiddatum|dossierNumber|Dossier|classification|Zusatzeigenschaft|indexCode|Quelle|dossierObject|Betreff|law|Rechtsgebiet|shortText|Vorschautext|department|Gericht|createDate|Erfasst am|creater|Ersteller|judge|Richter|executiontype|Erledigungsart|legalDate|Rechtskraftdatum|objecttype|Objekttyp|typist|Schreiber|description|Beschreibung|reference|Referenz|relevance|Relevanz|de|1|2|3|4|41|5|5|6|7|6|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|5|8|8|5|5|5|5|7|9|9|5|5|5|5|5|5|5|10|11|6|0|0|6|5|5|12|5|13|5|14|5|15|5|16|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|17|1|{page_nr}|18|19|20|21|0|22|5|5|23|5|24|5|25|5|26|5|27|5|10|5|28|5|29|5|30|5|31|22|18|5|32|5|33|5|34|5|35|5|36|5|37|5|38|5|39|5|40|5|41|5|42|5|43|5|44|5|45|5|46|5|47|5|48|5|49|5|50|5|51|5|52|5|53|5|54|5|55|5|56|5|57|5|58|5|59|5|60|5|61|5|62|5|63|5|64|5|65|5|66|5|67|10|68|10|10|11|11|0|'''
	HEADERS = { 'Content-type': 'text/x-gwt-rpc; charset=utf-8'
			  , 'X-GWT-Permutation': 'C56BCDCE0FCCE64CB5164DE7BBAF017B'
			  , 'X-GWT-Module-Base': 'https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/'
			  }
	MINIMUM_PAGE_LEN = 148
	DOWNLOAD_URL = 'https://www.zsg-entscheide.apps.be.ch/tribunapublikation/tribunavtplus/ServletDownload/'
	MAX_PAGES = 10
	reVor=re.compile('//OK\\[[0-9,\\.]+\\[')
	reAll=re.compile('(?<=,\\")[^\\"]*(?:\\\\\\"[^\\"]*)*(?=\\",)')
	reID=re.compile('[0-9a-f]{32}')
	reNum=re.compile('\D{2,3}\s\d\d\d\d\s\d+')
	reDatum=re.compile('\d{4}-\d{2}-\d{2}')
	reRG=re.compile('[^0-9\\.:-]{3}.{3,}')
	reTreffer=re.compile('(?<=^//OK\\[)[0-9]+')
	page_nr=0
	trefferzahl=0
	
	def get_next_request(self):
		if self.ab is None:
			body = BernSpider.RESULT_QUERY_TPL.format(page_nr=self.page_nr)
		else:
			body = BernSpider.RESULT_QUERY_TPL_AB.format(page_nr=self.page_nr, datum=self.ab)
		self.page_nr=self.page_nr+1
		return body	
	
	def request_generator(self):
		""" Generates scrapy frist request
		"""
		body=self.get_next_request()
		return [scrapy.Request(url=BernSpider.RESULT_PAGE_URL, method="POST", body=body, headers=BernSpider.HEADERS, callback=self.parse_page, errback=self.errback_httpbin)]

	def __init__(self,ab=None):
		super().__init__()
		self.ab = ab
		self.request_gen = self.request_generator()

	def start_requests(self):
		# treat the first request, subsequent ones are generated and processed inside the callback
		for request in self.request_gen:
			yield request
		logging.info("Normal beendet")

	def parse_page(self, response):	
		""" Parses the current search result page, downloads documents and yields the request for the next search
		result page
		"""
	
		if response.status == 200 and len(response.body) > BernSpider.MINIMUM_PAGE_LEN:
			# construct and download document links
			logging.info("Rohergebnis: "+response.body_as_unicode())
			if self.page_nr==1:
				treffer=self.reTreffer.search(response.body_as_unicode())
				if treffer:
					logging.info("Trefferzahl: "+treffer.group())
					self.trefferzahl=int(treffer.group())
			
			content = self.reVor.sub('',response.body_as_unicode())
			
			logging.info("Ergebnisseite: "+content)

			werte=self.reAll.findall(content)
			i=0
			for wert in werte:
				logging.info("Wert " +str(i)+": "+ wert)
				i=i+1

			brauchbar=True
			kammer=werte[3]
			id_=werte[5]
			titel=werte[6]
			num=werte[7]
			entscheiddatum=werte[8]
			leitsatz=werte[9]
			rechtsgebiet=werte[13]
			publikationsdatum=werte[len(werte)-1]
			if self.reDatum.fullmatch(publikationsdatum)==None: publikationsdatum=werte[len(werte)-2]
			
			if len(kammer)<11:
				logging.warning("Type mismatch keine Kammer '"+kammer+"'")
				kammer=""
			if self.reID.fullmatch(id_)==None:
				logging.warning("Type mismatch keine ID '"+id_+"'")	
				brauchbar=False
			if len(titel)<11:
				logging.warning("Type mismatch keine Titel '"+titel+"'")
				titel=""	 
			if self.reNum.fullmatch(num)==None:
				logging.warning("Type mismatch keine Geschäftsnummer '"+num+"'")
				brauchbar=False
			if self.reDatum.fullmatch(entscheiddatum)==None:
				logging.warning("Type mismatch keine Entscheiddatum '"+entscheiddatum+"'")
				brauchbar=False
			if len(leitsatz)<11:
				if leitsatz != '-':
					logging.warning("Type mismatch kein Leitsatz '"+leitsatz+"'")
				leitsatz=""
			if self.reRG.fullmatch(rechtsgebiet)==None:
				logging.warning("Type mismatch kein Rechtsgebiet '"+rechtsgebiet+"'")
				rechtsgebiet=""			   
			if self.reDatum.fullmatch(publikationsdatum)==None:
				logging.warning("Type mismatch letzter und vorletzter Eintrag kein Publikationsdatum '"+publikationsdatum+"'")
				publikationsdatum=""

			if brauchbar:
				numstr = num.replace(" ", "_")
				path_ = 'E%3A%5C%5Cwebapps%5C%5Ca2y%5C%5Ca2ya-www-trbpub100web%5C%5Cpdf%5C'
				href = "{}{}_{}.pdf?path={}\\{}.pdf&dossiernummer={}".format(BernSpider.DOWNLOAD_URL, numstr, id_,path_, id_, numstr)
				yield {
					'Kanton': 'Bern',
					'Num':num ,
					'Kammer':kammer,
					'EDatum': entscheiddatum,
					'PDatum': publikationsdatum,
					'Titel': titel,
					'Leitsatz': leitsatz,
					'Rechtsgebiet': rechtsgebiet,
					'DocId':id_,
					'PDFUrl': [href],
					'Raw': content
				}

				if self.page_nr < min(self.trefferzahl, self.MAX_PAGES):
					body = self.get_next_request()
					yield scrapy.Request(url=BernSpider.RESULT_PAGE_URL, method="POST", body=body, headers=BernSpider.HEADERS, callback=self.parse_page, errback=self.errback_httpbin)
		else:
			logging.error("ungültige Antwort")
			
			
	def errback_httpbin(self, failure):
		# log all errback failures,
		# in case you want to do something special for some errors,
		# you may need the failure's type
		logging.error(repr(failure))

 