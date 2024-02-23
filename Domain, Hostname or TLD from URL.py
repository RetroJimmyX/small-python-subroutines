# Acknowledgement for public suffix list (PSL): https://github.com/publicsuffix/

import requests
html = requests.get('https://publicsuffix.org/list/public_suffix_list.dat')
valid_domains  = [line for line in html.text.splitlines() if line != "" and line[:2] != "//"]
valid_domains += ["co.za","za"] # Fix for .co.za not present

def domain_name(url,output="d"):
  '''Returns the hostname (h), domain name (d) or TLD (t) as specified in the optional output
  for a URL containing a valid domain provided with/out protocol, sudomains or directories'''
  fqdn_arr = [x for x in url.split("/") if "." in x][0].split(".")[::-1]  # Extract FQDN as reversed ([::-1]) array; [0] because dir's can have a "."
  domain , i = fqdn_arr[0] , 0                                            # Build domain from comparison
  while domain in valid_domains:                                          # against TLD list and exclude
          i += 1                                                          # any subdomain(s)
          domain = fqdn_arr[i] + "." + domain
  if output == "h": return domain[:domain.index(".")]                     # return hostname (domain - TLD) 
  elif output == "t": return domain[domain.index("."):]                   # return tld (domain - hostname) 
  else: return domain                                                     # return domain by default    
