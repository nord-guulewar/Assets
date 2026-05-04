export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-700">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold text-slate-900 dark:text-white">Olaleye</h1>
              <p className="text-sm text-slate-600 dark:text-slate-400">Infosec Specialist</p>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <a href="#home" className="text-slate-900 dark:text-white hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">Home</a>
                <a href="#about" className="text-slate-600 dark:text-slate-400 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">About</a>
                <a href="#skills" className="text-slate-600 dark:text-slate-400 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">Skills</a>
                <a href="#projects" className="text-slate-600 dark:text-slate-400 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">Projects</a>
                <a href="#contact" className="text-slate-600 dark:text-slate-400 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">Contact</a>
              </div>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero */}
        <section id="home" className="py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-slate-900 dark:text-white mb-6">
              Infosec Specialist
            </h1>
            <p className="text-xl text-slate-600 dark:text-slate-400 mb-8 max-w-3xl mx-auto">
              Helping teams resolve security incidents, improve support processes, and communicate risk clearly while driving customer value.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="/resume.html" className="bg-slate-900 dark:bg-slate-700 text-white px-6 py-3 rounded-lg hover:bg-slate-800 transition-colors">
                📄 View Resume
              </a>
              <a href="#contact" className="border border-slate-300 dark:border-slate-600 text-slate-900 dark:text-white px-6 py-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors">
                Let&apos;s Connect
              </a>
            </div>
          </div>
        </section>

        {/* About */}
        <section id="about" className="py-16">
          <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6">About Me</h2>
            <p className="text-slate-600 dark:text-slate-400 text-lg leading-relaxed">
              I'm an infosec support professional with strong sales skills, focused on incident response, security collaboration, knowledge transfer, and translating technical risk into practical business outcomes.
            </p>
            <div className="mt-6 grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Skills</h3>
                <ul className="text-slate-600 dark:text-slate-400 space-y-1">
                  <li>• Phone/chat/email support</li>
                  <li>• Incident triage & escalation</li>
                  <li>• SLA management</li>
                  <li>• Product onboarding</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Certifications</h3>
                <ul className="text-slate-600 dark:text-slate-400 space-y-1">
                  <li>• Cisco Certified Ethical Hacker</li>
                  <li>• Critical Infrastructure Protection</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Skills */}
        <section id="skills" className="py-16">
          <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6">Infosec Support Strengths</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🛡️</span>
                </div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Incident Response</h3>
                <p className="text-slate-600 dark:text-slate-400">Rapid triage and resolution of security incidents</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Process Optimization</h3>
                <p className="text-slate-600 dark:text-slate-400">Streamlining workflows for better efficiency</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">💬</span>
                </div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Risk Communication</h3>
                <p className="text-slate-600 dark:text-slate-400">Translating technical risk to business impact</p>
              </div>
            </div>
          </div>
        </section>

        {/* Projects */}
        <section id="projects" className="py-16">
          <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6">Security Projects & Tools</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <a href="/tpm-guardian.html" className="block bg-slate-50 dark:bg-slate-700 rounded-lg p-6 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">🛡️ TPM-Less Guardian</h3>
                <p className="text-slate-600 dark:text-slate-400">Software-based file integrity monitoring</p>
              </a>
              <a href="/url-scanner.html" className="block bg-slate-50 dark:bg-slate-700 rounded-lg p-6 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">🎣 Phishing URL Scanner</h3>
                <p className="text-slate-600 dark:text-slate-400">Real-time URL risk analysis</p>
              </a>
              <a href="/ir-simulator.html" className="block bg-slate-50 dark:bg-slate-700 rounded-lg p-6 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">💀 IR Bot Stress Test</h3>
                <p className="text-slate-600 dark:text-slate-400">Incident response decision simulator</p>
              </a>
              <a href="/attack-map.html" className="block bg-slate-50 dark:bg-slate-700 rounded-lg p-6 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">🌍 Attack Surface Map</h3>
                <p className="text-slate-600 dark:text-slate-400">Interactive 3D asset vulnerability map</p>
              </a>
            </div>
            <div className="mt-8 text-center">
              <a href="/works.html" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
                View Case Studies →
              </a>
            </div>
          </div>
        </section>

        {/* Contact */}
        <section id="contact" className="py-16">
          <div className="bg-white dark:bg-slate-800 rounded-xl p-8 shadow-lg">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6">Get In Touch</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-4">Connect with me</h3>
                <div className="space-y-3">
                  <a href="https://github.com/nord-guulewar/mywebsite_portfolio" className="flex items-center text-slate-600 dark:text-slate-400 hover:text-blue-600">
                    <span className="mr-2">🐙</span> GitHub
                  </a>
                  <a href="https://instagram.com/aderopoola?igsh=dXZscmRzODBrZ2Ez" className="flex items-center text-slate-600 dark:text-slate-400 hover:text-blue-600">
                    <span className="mr-2">📸</span> Instagram
                  </a>
                  <a href="https://x.com/OmoObaAderopo" className="flex items-center text-slate-600 dark:text-slate-400 hover:text-blue-600">
                    <span className="mr-2">🐦</span> Twitter
                  </a>
                  <a href="mailto:olaleyelekanjoseph@gmail.com" className="flex items-center text-slate-600 dark:text-slate-400 hover:text-blue-600">
                    <span className="mr-2">✉️</span> Email
                  </a>
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-4">Quick Message</h3>
                <form className="space-y-4">
                  <div>
                    <input type="text" placeholder="Name" className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white" />
                  </div>
                  <div>
                    <input type="email" placeholder="Email" className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white" />
                  </div>
                  <div>
                    <textarea placeholder="Message" rows={4} className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white"></textarea>
                  </div>
                  <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    Send Message
                  </button>
                </form>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 dark:bg-black text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>© 2026 Olaleye • Infosec Portfolio</p>
        </div>
      </footer>
    </div>
  );
}
