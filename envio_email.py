# -*- coding: utf-8 -*-

__author__ = "Danilo Vaz"
__copyright__ = "Copyright 2015, DWrobot"
__credits__ = ["Danilo Vaz"]
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Danilo Vaz"
__email__ = "danilovazb@gmail.com"
__status__ = "Beta"

import smtplib
import sys
import commands
from email.MIMEText import MIMEText

class enviaEmail(object):
	def __init__(self,erro,email):
		self.erro = erro
		self.email = email

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# - Faz o envio do email de erro com o HTML abaixo						 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	def envia_email(self):
		try :
			serv=smtplib.SMTP()
			smtpserver="smtp.ifractal.com.br"
			serv.connect(smtpserver,587)
			serv.login("danilo.vaz@ifractal.com.br","Seila!+123")
			html = """
			<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
		<html xmlns='http://www.w3.org/1999/xhtml'>
		    <head>
		      <!-- NAME: 1 COLUMN - BANDED -->
		        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
		        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
		        
		    <style type='text/css'>
		    body,#bodyTable,#bodyCell{
		      height:100% !important;
		      margin:0;
		      padding:0;
		      width:100% !important;
		    }
		    table{
		      border-collapse:collapse;
		    }
		    img,a img{
		      border:0;
		      outline:none;
		      text-decoration:none;
		    }
		    h1,h2,h3,h4,h5,h6{
		      margin:0;
		      padding:0;
		    }
		    p{
		      margin:1em 0;
		      padding:0;
		    }
		    a{
		      word-wrap:break-word;
		    }
		    .ReadMsgBody{
		      width:100%;
		    }
		    .ExternalClass{
		      width:100%;
		    }
		    .ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{
		      line-height:100%;
		    }
		    table,td{
		      mso-table-lspace:0pt;
		      mso-table-rspace:0pt;
		    }
		    #outlook a{
		      padding:0;
		    }
		    img{
		      -ms-interpolation-mode:bicubic;
		    }
		    body,table,td,p,a,li,blockquote{
		      -ms-text-size-adjust:100%;
		      -webkit-text-size-adjust:100%;
		    }
		    #bodyCell{
		      padding:0;
		    }
		    .mcnImage{
		      vertical-align:bottom;
		    }
		    .mcnTextContent img{
		      height:auto !important;
		    }
		    body,#bodyTable{
		      background-color:#F2F2F2;
		    }
		    #bodyCell{
		      border-top:0;
		    }
		    h1{
		      color:#606060 !important;
		      display:block;
		      font-family:Helvetica;
		      font-size:40px;
		      font-style:normal;
		      font-weight:bold;
		      line-height:125%;
		      letter-spacing:-1px;
		      margin:0;
		      text-align:left;
		    }
		    h2{
		      color:#404040 !important;
		      display:block;
		      font-family:Helvetica;
		      font-size:26px;
		      font-style:normal;
		      font-weight:bold;
		      line-height:125%;
		      letter-spacing:-.75px;
		      margin:0;
		      text-align:left;
		    }
		    h3{
		      color:#606060 !important;
		      display:block;
		      font-family:Helvetica;
		      font-size:18px;
		      font-style:normal;
		      font-weight:bold;
		      line-height:125%;
		      letter-spacing:-.5px;
		      margin:0;
		      text-align:left;
		    }
		    h4{
		      color:#808080 !important;
		      display:block;
		      font-family:Helvetica;
		      font-size:16px;
		      font-style:normal;
		      font-weight:bold;
		      line-height:125%;
		      letter-spacing:normal;
		      margin:0;
		      text-align:left;
		    }
		    #templatePreheader{
		      background-color:#FFFFFF;
		      border-top:0;
		      border-bottom:0;
		    }
		    .preheaderContainer .mcnTextContent,.preheaderContainer .mcnTextContent p{
		      color:#606060;
		      font-family:Helvetica;
		      font-size:11px;
		      line-height:125%;
		      text-align:left;
		    }
		    .preheaderContainer .mcnTextContent a{
		      color:#606060;
		      font-weight:normal;
		      text-decoration:underline;
		    }
		    #templateHeader{
		      background-color:#FFFFFF;
		      border-top:0;
		      border-bottom:0;
		    }
		    .headerContainer .mcnTextContent,.headerContainer .mcnTextContent p{
		      color:#606060;
		      font-family:Helvetica;
		      font-size:15px;
		      line-height:150%;
		      text-align:left;
		    }
		    .headerContainer .mcnTextContent a{
		      color:#6DC6DD;
		      font-weight:normal;
		      text-decoration:underline;
		    }
		    #templateBody{
		      background-color:#FFFFFF;
		      border-top:0;
		      border-bottom:0;
		    }
		    .bodyContainer .mcnTextContent,.bodyContainer .mcnTextContent p{
		      color:#606060;
		      font-family:Helvetica;
		      font-size:15px;
		      line-height:150%;
		      text-align:left;
		    }
		    .bodyContainer .mcnTextContent a{
		      color:#6DC6DD;
		      font-weight:normal;
		      text-decoration:underline;
		    }
		    #templateFooter{
		      background-color:#F2F2F2;
		      border-top:0;
		      border-bottom:0;
		    }
		    .footerContainer .mcnTextContent,.footerContainer .mcnTextContent p{
		      color:#606060;
		      font-family:Helvetica;
		      font-size:11px;
		      line-height:125%;
		      text-align:left;
		    }
		    .footerContainer .mcnTextContent a{
		      color:#606060;
		      font-weight:normal;
		      text-decoration:underline;
		    }
		  @media only screen and (max-width: 480px){
		    body,table,td,p,a,li,blockquote{
		      -webkit-text-size-adjust:none !important;
		    }

		} @media only screen and (max-width: 480px){
		    body{
		      width:100% !important;
		      min-width:100% !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=mcnTextContentContainer]{
		      width:100% !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=mcnBoxedTextContentContainer]{
		      width:100% !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=mcpreview-image-uploader]{
		      width:100% !important;
		      display:none !important;
		    }

		} @media only screen and (max-width: 480px){
		    img[class=mcnImage]{
		      width:100% !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=mcnImageGroupContentContainer]{
		      width:100% !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnImageGroupContent]{
		      padding:9px !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnImageGroupBlockInner]{
		      padding-bottom:0 !important;
		      padding-top:0 !important;
		    }

		} @media only screen and (max-width: 480px){
		    tbody[class=mcnImageGroupBlockOuter]{
		      padding-bottom:9px !important;
		      padding-top:9px !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=mcnCaptionTopContent],table[class=mcnCaptionBottomContent]{
		      width:100% !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=mcnCaptionLeftTextContentContainer],table[class=mcnCaptionRightTextContentContainer],table[class=mcnCaptionLeftImageContentContainer],table[class=mcnCaptionRightImageContentContainer],table[class=mcnImageCardLeftTextContentContainer],table[class=mcnImageCardRightTextContentContainer]{
		      width:100% !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
		      padding-right:18px !important;
		      padding-left:18px !important;
		      padding-bottom:0 !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnImageCardBottomImageContent]{
		      padding-bottom:9px !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnImageCardTopImageContent]{
		      padding-top:18px !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
		      padding-right:18px !important;
		      padding-left:18px !important;
		      padding-bottom:0 !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnImageCardBottomImageContent]{
		      padding-bottom:9px !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnImageCardTopImageContent]{
		      padding-top:18px !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=mcnCaptionLeftContentOuter] td[class=mcnTextContent],table[class=mcnCaptionRightContentOuter] td[class=mcnTextContent]{
		      padding-top:9px !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnCaptionBlockInner] table[class=mcnCaptionTopContent]:last-child td[class=mcnTextContent]{
		      padding-top:18px !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnBoxedTextContentColumn]{
		      padding-left:18px !important;
		      padding-right:18px !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=mcnTextContent]{
		      padding-right:18px !important;
		      padding-left:18px !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=templateContainer]{
		      max-width:600px !important;
		      width:100% !important;
		    }

		} @media only screen and (max-width: 480px){
		    h1{
		      font-size:24px !important;
		      line-height:125% !important;
		    }

		} @media only screen and (max-width: 480px){
		    h2{
		      font-size:20px !important;
		      line-height:125% !important;
		    }

		} @media only screen and (max-width: 480px){
		    h3{
		      font-size:18px !important;
		      line-height:125% !important;
		    }

		} @media only screen and (max-width: 480px){
		    h4{
		      font-size:16px !important;
		      line-height:125% !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[class=mcnBoxedTextContentContainer] td[class=mcnTextContent],td[class=mcnBoxedTextContentContainer] td[class=mcnTextContent] p{
		      font-size:18px !important;
		      line-height:125% !important;
		    }

		} @media only screen and (max-width: 480px){
		    table[id=templatePreheader]{
		      display:block !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=preheaderContainer] td[class=mcnTextContent],td[class=preheaderContainer] td[class=mcnTextContent] p{
		      font-size:14px !important;
		      line-height:115% !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=headerContainer] td[class=mcnTextContent],td[class=headerContainer] td[class=mcnTextContent] p{
		      font-size:18px !important;
		      line-height:125% !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=bodyContainer] td[class=mcnTextContent],td[class=bodyContainer] td[class=mcnTextContent] p{
		      font-size:18px !important;
		      line-height:125% !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=footerContainer] td[class=mcnTextContent],td[class=footerContainer] td[class=mcnTextContent] p{
		      font-size:14px !important;
		      line-height:115% !important;
		    }

		} @media only screen and (max-width: 480px){
		    td[class=footerContainer] a[class=utilityLink]{
		      display:block !important;
		    }

		}</style></head>
		    <body leftmargin='0' marginwidth='0' topmargin='0' marginheight='0' offset='0' style='margin: 0;padding: 0;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #F2F2F2;height: 100% !important;width: 100% !important;'>
		        <center>
		            <table align='center' border='0' cellpadding='0' cellspacing='0' height='100%' width='100%' id='bodyTable' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;margin: 0;padding: 0;background-color: #F2F2F2;height: 100% !important;width: 100% !important;'>
		                <tr>
		                    <td align='center' valign='top' id='bodyCell' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;margin: 0;padding: 0;border-top: 0;height: 100% !important;width: 100% !important;'>
		                        <!-- BEGIN TEMPLATE // -->
		                        <table border='0' cellpadding='0' cellspacing='0' width='100%' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                            <tr>
		                                <td align='center' valign='top' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                    <!-- BEGIN PREHEADER // -->
		                                    <table border='0' cellpadding='0' cellspacing='0' width='100%' id='templatePreheader' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;'>
		                                        <tr>
		                                          <td align='center' valign='top' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                                <table border='0' cellpadding='0' cellspacing='0' width='600' class='templateContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                                    <tr>
		                                                        <td valign='top' class='preheaderContainer' style='padding-top: 9px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'><table border='0' cellpadding='0' cellspacing='0' width='100%' class='mcnTextBlock' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		    <tbody class='mcnTextBlockOuter'>
		        <tr>
		            <td valign='top' class='mcnTextBlockInner' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                
		                <table align='left' border='0' cellpadding='0' cellspacing='0' width='366' class='mcnTextContentContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                    <tbody><tr>
		                        
		                        <td valign='top' class='mcnTextContent' style='padding-top: 9px;padding-left: 18px;padding-bottom: 9px;padding-right: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #606060;font-family: Helvetica;font-size: 11px;line-height: 125%;text-align: left;'>
		                        
		                            
		                        </td>
		                    </tr>
		                </tbody></table>
		                
		                <table align='right' border='0' cellpadding='0' cellspacing='0' width='197' class='mcnTextContentContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                    <tbody><tr>
		                        
		                        <td valign='top' class='mcnTextContent' style='padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #606060;font-family: Helvetica;font-size: 11px;line-height: 125%;text-align: left;'>
		                        
		                            
		                        </td>
		                    </tr>
		                </tbody></table>
		                
		            </td>
		        </tr>
		    </tbody>
		</table></td>
		                                                    </tr>
		                                                </table>
		                                            </td>                                            
		                                        </tr>
		                                    </table>
		                                    <!-- // END PREHEADER -->
		                                </td>
		                            </tr>
		                            <tr>
		                                <td align='center' valign='top' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                    <!-- BEGIN HEADER // -->
		                                    <table border='0' cellpadding='0' cellspacing='0' width='100%' id='templateHeader' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;'>
		                                        <tr>
		                                            <td align='center' valign='top' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                                <table border='0' cellpadding='0' cellspacing='0' width='600' class='templateContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                                    <tr>
		                                                        <td valign='top' class='headerContainer' style='padding-top: 10px;padding-bottom: 10px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'><table border='0' cellpadding='0' cellspacing='0' width='100%' class='mcnImageBlock' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		    <tbody class='mcnImageBlockOuter'>
		            <tr>
		                <td valign='top' style='padding: 0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;' class='mcnImageBlockInner'>
		                    <table align='left' width='100%' border='0' cellpadding='0' cellspacing='0' class='mcnImageContentContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                        <tbody><tr>
		                            <td class='mcnImageContent' valign='top' style='padding-right: 0px;padding-left: 0px;padding-top: 0;padding-bottom: 0;text-align: center;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                
		                                    <a href='#' title='' class='' target='_blank' style='word-wrap: break-word;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                        <img align='center' alt='' src='https://gallery.mailchimp.com/4e8abfd6680f5b91d3fc5e69e/images/382587a1-a44a-4753-8ef5-dc605d02b819.png' width='384' style='max-width: 768px;padding-bottom: 0;display: inline !important;vertical-align: bottom;border: 0;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;' class='mcnImage'></a>
		                                
		                            </td>
		                        </tr>
		                    </tbody></table>
		                </td>
		            </tr>
		    </tbody>
		</table></td>
		                                                    </tr>
		                                                </table>
		                                            </td>
		                                        </tr>
		                                    </table>
		                                    <!-- // END HEADER -->
		                                </td>
		                            </tr>
		                            <tr>
		                                <td align='center' valign='top' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                    <!-- BEGIN BODY // -->
		                                    <table border='0' cellpadding='0' cellspacing='0' width='100%' id='templateBody' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;'>
		                                        <tr>
		                                            <td align='center' valign='top' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                                <table border='0' cellpadding='0' cellspacing='0' width='600' class='templateContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                                    <tr>
		                                                        <td valign='top' class='bodyContainer' style='padding-top: 10px;padding-bottom: 10px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'><table border='0' cellpadding='0' cellspacing='0' width='100%' class='mcnTextBlock' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		    <tbody class='mcnTextBlockOuter'>
		        <tr>
		            <td valign='top' class='mcnTextBlockInner' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                
		                <table align='left' border='0' cellpadding='0' cellspacing='0' width='600' class='mcnTextContentContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                    <tbody><tr>
		                        
		                        <td valign='top' class='mcnTextContent' style='padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #606060;font-family: Helvetica;font-size: 15px;line-height: 150%;text-align: left;'>
		                        
		                            <h1 style='margin: 0;padding: 0;display: block;font-family: Helvetica;font-size: 40px;font-style: normal;font-weight: bold;line-height: 125%;letter-spacing: -1px;text-align: left;color: #606060 !important;'><span style='color:#FF0000'><img align='none' height='33' src='https://gallery.mailchimp.com/4e8abfd6680f5b91d3fc5e69e/images/6bafc20f-82c6-4274-a406-e5ecdfed86dd.png' style='width: 40px;height: 33px;margin: 0px;border: 0;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;' width='40'>&nbsp;ERRO!</span></h1>

		<p style='margin: 1em 0;padding: 0;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #606060;font-family: Helvetica;font-size: 15px;line-height: 150%;text-align: left;'>Descrição:<br> """

			html2 = """
		&nbsp;</p>

		                        </td>
		                    </tr>
		                </tbody></table>
		                
		            </td>
		        </tr>
		    </tbody>
		</table></td>
		                                                    </tr>
		                                                </table>
		                                            </td>
		                                        </tr>
		                                    </table>
		                                    <!-- // END BODY -->
		                                </td>
		                            </tr>
		                            <tr>
		                                <td align='center' valign='top' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                    <!-- BEGIN FOOTER // -->
		                                    <table border='0' cellpadding='0' cellspacing='0' width='100%' id='templateFooter' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #F2F2F2;border-top: 0;border-bottom: 0;'>
		                                        <tr>
		                                            <td align='center' valign='top' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                                <table border='0' cellpadding='0' cellspacing='0' width='600' class='templateContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                                                    <tr>
		                                                        <td valign='top' class='footerContainer' style='padding-top: 10px;padding-bottom: 10px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'><table border='0' cellpadding='0' cellspacing='0' width='100%' class='mcnTextBlock' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		    <tbody class='mcnTextBlockOuter'>
		        <tr>
		            <td valign='top' class='mcnTextBlockInner' style='mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                
		                <table align='left' border='0' cellpadding='0' cellspacing='0' width='600' class='mcnTextContentContainer' style='border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'>
		                    <tbody><tr>
		                        
		                        <td valign='top' class='mcnTextContent' style='padding: 9px 18px;text-align: left;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #606060;font-family: Helvetica;font-size: 11px;line-height: 125%;'>
		                        
		                            
		                        </td>
		                    </tr>
		                </tbody></table>
		                
		            </td>
		        </tr>
		    </tbody>
		</table></td>
		                                                    </tr>
		                                                </table>
		                                            </td>
		                                        </tr>
		                                    </table>
		                                    <!-- // END FOOTER -->
		                                </td>
		                            </tr>
		                        </table>
		                        <!-- // END TEMPLATE -->
		                    </td>
		                </tr>
		            </table>
		        </center>
		    </body>
		</html>
		"""
			html_tudo = str(html) + str(self.erro) + str(html2)
			msg1 = MIMEText(str(html_tudo),'html')
			msg1['Subject']='ERRO Processo de download XML'
			msg1['From']="danilo.vaz@ifractal.com.br"
			msg1['To']="danilo.vaz@ifractal.com.br"
			serv.sendmail("danilo.vaz@ifractal.com.br","danilo.vaz@ifractal.com.br", msg1.as_string())
			#serv.sendmail("danilo.vaz@ifractal.com.br","cristiano@ifractal.com.br", msg1.as_string())
			serv.sendmail("danilo.vaz@ifractal.com.br","arthur@ifractal.com.br", msg1.as_string())
			serv.quit()
		except Exception, e:
			print "Erro : %s" % e
		else:
			print "Concluido"
