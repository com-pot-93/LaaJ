require "fileutils"
require 'typhoeus'
require 'curb'
require "ferrum"

instance_number = '9734'

def cpee_to_bpmn(file_path,run,browser,instance_number)
  puts "Processing file: #{file_path}"
  c = Curl::Easy.new("https://autobpmn.ai/flow/engine/#{instance_number}/properties/dslx/")
  c.multipart_form_post = true
  puts "HERE"
  c.http_put(Curl::PostField.file("dslx", file_path, "text/xml"))
  puts "Status: #{c.response_code}"
  puts "Body: #{c.body_str}"
  sleep 1
  puts "HERE222222222"
  newbutton = browser.at_css("button[name='savebpmnfile']")
  browser.downloads.wait { newbutton.click }
  download_dir = File.join(run, "*")
  puts download_dir
  puts "Here 55555555555555"
  downloaded_file = Dir[download_dir].max_by { |f| File.mtime(f) }
  puts "THERE 3333333333333333"
  pp downloaded_file
  if downloaded_file
    new_name = File.join(run, file_path.split("/")[-1].sub(".xml", ".bpmn"))
    File.rename(downloaded_file, new_name)
    puts "Saved file as #{new_name}"
  else
    puts "No file downloaded"
  end
end



browser = Ferrum::Browser.new(browser_path: "/home/i17/projects/SAP/t2p_clean/src/chrome/linux-140.0.7339.207/chrome-linux64/chrome")
browser.goto("https://autobpmn.ai/flow/?monitor=https://autobpmn.ai/flow/engine/#{instance_number}/")
#browser.downloads.set_behavior(save_path: "/home/i17/projects/SAP/support-text2process-evaluation/downloads", behavior: :allowAndName)
checkbox = browser.at_css("input[type='checkbox']#iagree") # adjust selector
checkbox.click
button = browser.at_css("button#icontinue")
button.click
browser.network.wait_for_idle
sleep 2

folder_path = "datasets"
sets = ['mad150','domain','sapsam','pet','realset']
for s in sets do
  puts s
  approaches = Dir.glob(File.join("..",'..',"text2process-evaluation",folder_path, s, "generations"))
  apps = Dir.glob(File.join(approaches, "*")).select{ |path| File.directory?(path)}
  for app in apps do
    if app.include?("autobpmn")
      puts '***'
      runs = Dir.glob(File.join(app, "*")).select{ |path| File.directory?(path)}
      for run in runs do
        if run.include?("gpt-4o_r1")
          absolute = File.expand_path(run)
          puts run
          puts absolute
          browser.downloads.set_behavior(save_path: absolute, behavior: :allowAndName)
          txt_files = Dir.glob(File.join(run, "*.xml"))
          txt_files.each do |file_path|
            pp file_path
            cpee_to_bpmn(file_path,run,browser,instance_number)
          end
        end
      end
    end
  end
end

browser.quit



